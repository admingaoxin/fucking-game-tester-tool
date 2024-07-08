import rdtest
import os
import random
import struct
from typing import List
import renderdoc as rd
from rdtest import analyse
import pprint
def _print(s):
    pass

def save_texture(controller,texsave: rd.TextureSave,name):
    if texsave.resourceId == rd.ResourceId.Null():
        return

    texsave.comp.blackPoint = 0.0
    texsave.comp.whitePoint = 1.0
    texsave.alpha = rd.AlphaMapping.BlendToCheckerboard
    name  = name.replace(":","")
    filename = rdtest.get_tmp_path(name)
    rdtest.log.print(f"Saving image of {str(texsave.resourceId)}    {filename}")
    #texsave.destType = rd.FileType.HDR
    #controller.SaveTexture(texsave, filename + ".hdr")

    texsave.destType = rd.FileType.JPG
    filename  = filename + ".jpg"
    #controller.SaveTexture(texsave, filename)
    return filename
    texsave.mip = -1
    texsave.slice.sliceIndex = -1

    texsave.destType = rd.FileType.DDS
    controller.SaveTexture(texsave, filename + ".dds")
    return filename

class Writer:
    class Sub:
        def __init__(self,sup,n,ary = False,noapd = False,parent = None):
            self.sup = sup
            self.n   = n
            self.ary_mode = ary
            self.noapd = noapd
            self.parent = parent
        def __enter__(self):
            p = self.parent
            sup  = self.sup
            if self.ary_mode:
                sup.curr[self.n] = []
                sup.ary   = sup.curr[self.n]
                sup.stack.append(sup.curr)
                sup.curr = None
                sup.arycurr = {}
            elif p.ary_mode:
                sup.curr =  {}
            else:
                if self.n not in sup.curr:
                    sup.curr[self.n] = {}
                sup.stack.append(sup.curr)
                sup.curr    = sup.curr[self.n]

            return sup
        def __exit__(self, exc_type, exc_val, exc_tb):
            sup = self.sup
            p = self.parent
            if self.ary_mode:
                sup.curr = sup.stack.pop()
                self.ary_mode = False
            elif p.ary_mode:
                sup.arycurr[self.n] = sup.curr
                if not self.noapd:
                    sup.ary.append(sup.arycurr)
                    sup.arycurr = {}
            else:
                sup.curr = sup.stack.pop()
            sup.pChain.pop()

    def __init__(self,file,out_path,controller):
        self.file = file
        self.out_path = out_path
        self.controller = controller
        self.D    = {}
        self.curr = self.D
        self.stack = []
        self.sub   = False
        self.ary_mode = False
        currentSub = Writer.Sub(self,"rootDummy",False,False,None)
        self.pChain = [currentSub]

    def varname( self,var, dir=None):
        if dir  is None:
            dir = globals()
        vars = [ key for key, val in dir.items() if id( val) == id( var)]
        print(vars)

    def beginSubTitle(self,n):
        currentSub = Writer.Sub(self,n,False,False,self.pChain[-1])
        self.pChain.append(currentSub)
        return currentSub
    def beginSubArray(self,n):
        self.ary = []
        self.ary_mode  = True
        currentSub = Writer.Sub(self,n,True,False,self.pChain[-1])
        self.pChain.append(currentSub)
        return currentSub
    def array_append(self,v):
        assert self.ary_mode
        self.ary.append(v)
    def beginSub(self,n,cls):
        self.cls = cls
        currentSub = Writer.Sub(self,n,False,False,self.pChain[-1])
        self.pChain.append(currentSub)
        return currentSub
    def beginSubNoAppend(self,n,cls):
        self.cls = cls
        currentSub = Writer.Sub(self,n,False,True,self.pChain[-1])
        self.pChain.append(currentSub)
        return currentSub

    def write(self,n):

        self.curr[n] = eval(f"self.cls.{n}")
    def print(self):
        pprint.pprint(self.D)
    def write_attribute(self,attr,bindings,buf):
        with self.beginSub(f"{attr.binding}-{attr.location}",attr) as w:
            w.write("location")
            w.write("binding")
            binding  = bindings[attr.binding]
            cbuf = buf[binding.vertexBufferBinding]
            _print(f"binding.vertexBufferBinding {binding.vertexBufferBinding}")
            self.write_binding("buffer",binding,cbuf)
            with self.beginSub("format",attr.format) as w:
                w.write("type")
                w.write("compCount")
                w.write("compType")
    def write_binding(self,name,binding,cbuf):
        binding.resourceId = cbuf.resourceId
        with self.beginSub(name,binding) as w:
            w.write("vertexBufferBinding")
            w.write("perInstance")
            w.write("instanceDivisor")
            w.write("resourceId")
    def write_resource_format(self,format):
        with self.beginSub("resource_format",format) as w:
            w.write("type")
            w.write("compCount")
            w.write("compByteWidth")
            w.write("compType")

    def write_attchment(self,name,at):
        if int(at.imageResourceId) == 0:
            return
        with self.beginSub(name,at) as w:
            w.write("imageResourceId")
            w.write("firstMip")
            w.write("numMips")
            w.write("firstSlice")
            w.write("numSlices")
            w.write("swizzle")
            w.write_resource_format(at.viewFormat)

    def write_signature(self,name,sig):
        with self.beginSub(name,sig) as w:
            w.write("varName")
            w.write("varType")
            w.write("compCount")
            w.write("semanticName")
            w.write("semanticIdxName")
            w.write("semanticIndex")
    def write_constant_variable(self,name,var):
        with self.beginSub(name,var) as w:
            w.write("compType.name")
            w.write("type.name")
            w.write("type.elements")
            w.write("byteOffset")
            w.write("bitFieldOffset")
            w.write("itemSize")
            w.write("count")
            w.write("arraySize")
            w.write("size")
            w.write("data")

    def write_shader_resource(self,name,res):
        with self.beginSub(name,res) as w:
            w.write("name")
            w.write("resType")
            w.write("variableType")
            w.write("bindPoint")
            w.write("isTexture")
            w.write("isReadOnly")
    def write_sampler(self,name,res,sampler,bound):
        with self.beginSub(name,sampler) as w:
            w.write("addressU")
            w.write("addressV")
            w.write("addressW")
            w.write("borderColor")
            w.write("compareFunction")
            # w.write("seamlessCubeMap")
            w.write("maxAnisotropy")
            w.write("maxLOD")
            w.write("minLOD")
            #w.write("mipLODBias")
            with self.beginSub("filter",sampler.filter) as w:
                w.write("minify")
                w.write("magnify")
                w.write("mip")
                w.write("filter")
            with self.beginSub("resource",res) as w:
                w.write("name")
                w.write("type")
                w.write("resourceId")
            with self.beginSub("bindpoint",bound.bindPoint) as w:
                w.write("used")
                w.write("bindset")
                w.write("bind")
                w.write("arraySize")
    def write_resource(self,name,id,tex_details,res_details):
        res_details.entrypoint = self.controller.GetShaderEntryPoints(id)
        res_details.usage = self.controller.GetUsage(id)
        with self.beginSub(name,tex_details) as w:
            w.write("width")
            w.write("height")
            w.write("dimension")
            with self.beginSub("resource",res_details ) as w:
                w.write("name")
                w.write("type")
                w.write("resourceId")
                w.write("entrypoint")
                w.write("usage")
    def write_data(self,Data):
        def rec(Data):
            for name,d in Data.items():
                if type(d) == bytes or type(d) == str:
                    with self.beginSub(str(name),d) as w:
                        self.curr["raw_data"] = d
                elif type(d) == dict:
                    with self.beginSubTitle(str(name)) as w:
                        rec(d)
                else:
                    with self.beginSub(str(name),d) as w:
                        w.write("itemSize")
                        w.write("cols")
                        w.write("rows")
                        w.write("arraySize")
                        w.write("size")
                        w.write("data")
        with self.beginSubTitle("Data") as w:
            rec(Data)
    def write_json(self):
        import json
        def dumper(obj):
            try:
                return obj.toJSON()
            except:
                #print(f"Not Serialized {obj} {type(obj)} ")
                return str(obj)

        with open(f"{self.out_path}/{self.file.name.replace('.rdc','.json')}", 'w') as f:
            json.dump(self.D, f,default=dumper,indent =4)

class Reader:
    def __init__(self,controller,state,vkstate,writer = None):
        self.controller =controller
        self.state = state
        self.vkstate = vkstate
        self.writer  = writer
    def check(self, expr, msg=None):
        if not expr:
            callstack = traceback.extract_stack()
            callstack.pop()
            assertion_line = callstack[-1].line

            assert_msg = re.sub(r'[^(]*\((.*)?\)', r'\1', assertion_line)

            if msg is None:
                raise TestFailureException('Assertion Failure: {}'.format(assert_msg))
            else:
                raise TestFailureException('Assertion Failure: {}'.format(msg))

class Output_Reader(Reader):
    def read(self):
        curpass: rd.VKCurrentPass = self.vkstate.currentPass
        with self.writer.beginSubTitle("Output") as w:
            fb = curpass.framebuffer
            rp = curpass.renderpass
            refl = self.state.GetShaderReflection(rd.ShaderStage.Fragment)
            with self.writer.beginSub("FrameBuffer",fb) as w1:
                w1.write("resourceId")
                w1.write("width")
                w1.write("height")
                with self.writer.beginSubArray("Signatures") as w0:
                    for sig in refl.outputSignature:
                        sig: rd.SigParameter
                        if sig.systemValue == rd.ShaderBuiltin.Position:
                            vsout_pos_name = sig.varName
                            if vsout_pos_name == '':
                                vsout_pos_name = sig.semanticName
                        self.writer.write_signature(sig.varName,sig)
                with self.writer.beginSubArray("Attchments") as w0:
                    for index in rp.colorAttachments:
                        im = fb.attachments[index]
                        self.writer.write_attchment("ColorAttchment",im)
                    if rp.depthstencilAttachment >= 0:
                        im =  fb.attachments[rp.depthstencilAttachment]
                        self.writer.write_attchment("depthstencilAttachment",im)
                    #im =  fb.attachments[rp.stencilAttachment]
                    #self.writer.write_attchment("StencilAttchment",im)
                with self.writer.beginSub("RenderPass",rp) as w:
                    w.write("resourceId")
                    w.write("feedbackLoop")
                    w.write("subpass")

        for index in rp.colorAttachments:
            im = fb.attachments[index]
            resourceId = im.imageResourceId
        if  rp.depthstencilAttachment  >= 0:
            im = fb.attachments[index]
            resourceId = im.imageResourceId

class Input_Reader(Reader):
    def read(self,action):
        with self.writer.beginSubTitle("Input") as w:
            ib: rd.BoundVBuffer  = self.controller.GetPipelineState().GetIBuffer()
            num_indices          = action.numIndices
            ioffs                = action.indexOffset * ib.byteStride
            mesh                 = rd.MeshFormat()
            mesh.numIndices      = num_indices
            mesh.indexByteOffset = ib.byteOffset + ioffs
            mesh.indexByteStride = ib.byteStride
            mesh.indexResourceId = ib.resourceId
            mesh.baseVertex      = action.baseVertex
            if ib.byteSize > ioffs:
                mesh.indexByteSize = ib.byteSize - ioffs
            else:
                mesh.indexByteSize = 0

            is_indexed = bool(action.flags & rd.ActionFlags.Indexed)
            if not (is_indexed):
                mesh.indexByteOffset = 0
                mesh.indexByteStride = 0
                mesh.indexResourceId = rd.ResourceId.Null()
            action.is_indexed = is_indexed
            with self.writer.beginSub("DrawCall",action) as w1:
                w1.write("is_indexed")
                w1.write("numIndices")
                w1.write("baseVertex")
                w1.write("vertexOffset")
                w1.write("numInstances")
                w1.write("instanceOffset")
                w1.write("indexOffset")

            attrs = analyse.get_vsin_attrs(self.controller, action.vertexOffset, mesh)
            if len(attrs) <= 0:
                return

            for attr in attrs:
                with self.writer.beginSub("Attribute",attr) as w2:
                    stride = attr.mesh.format.compByteWidth * attr.mesh.format.compCount
                    w2.write("name")
                    with self.writer.beginSub("mesh",attr.mesh) as w3:
                        w3.write("instStepRate")
                        w3.write("vertexByteSize")
                        w3.write("vertexByteOffset")
                        w3.write("vertexByteStride")
                        w3.write("vertexResourceId")
                        w3.write("format.compType.name")


            first_index = min(action.vertexOffset, action.numIndices-1)
            indices = analyse.fetch_indices(self.controller, action, mesh, 0, first_index, num_indices)
            mesh.data  = analyse.decode_mesh_data(self.controller, indices, indices, attrs, 0, 0)
            with self.writer.beginSub("mesh",mesh) as w:
                w.write("data")

class Rasterrizer_Reader(Reader):
    def checkEQ(self, v1,v2):
        print(f"Check Raster state  {v1}  ")
        #super().check(expr, msg)
    def depthStencil(self,de):
        with self.writer.beginSubTitle("DepthStencil") as w:
            with self.writer.beginSub("depthState",de) as w1:
                w1.write("depthTestEnable")
                w1.write("depthFunction")
                w1.write("depthWriteEnable")
                w1.write("depthBoundsEnable")
                w1.write("minDepthBounds")
                w1.write("maxDepthBounds")
            with self.writer.beginSub("stencilState",de) as w1:
                w1.write("stencilTestEnable")
                for Face in ["frontFace","backFace"]:
                    with self.writer.beginSub(Face,eval(f"de.{Face}")) as w2:
                        w2.write("failOperation")
                        w2.write("depthFailOperation")
                        w2.write("function")
                        w2.write("reference")
                        w2.write("compareMask")
                        w2.write("writeMask")
                        w2.write("passOperation")

    def rasterizer(self,ra,ms,co):
        with self.writer.beginSub("Rasterizer",ra) as w:
            w.write("fillMode")
            w.write("cullMode")
            w.write("frontCCW")
            w.write("depthClampEnable")

            w.write("depthBiasEnable")
            w.write("depthBias")
            w.write("depthBiasClamp") #w.write("offsetClamp")
            w.write("slopeScaledDepthBias")

            w.write("depthClampEnable")
            w.write("rasterizerDiscardEnable")

            w.write("lineWidth")
            w.write("lineRasterMode") # w.write("lineSmoothing") w.write("lineSmoothingEnabled")
            w.write("lineStippleFactor")
            w.write("lineStipplePattern")

            #w.write("programmablePointSize")
            #w.write("pointSize")
            #w.write("pointFadeThreshold")
            #w.write("pointOriginUpperLeft")

         #w.write("multisampleEnable")
        with self.writer.beginSub("Multisample",ms) as w:
            ms.multisampleEnable = True if ms.rasterSamples > 1 else False
            w.write("multisampleEnable")
            w.write("sampleShadingEnable")
            ms.alphaToCoverage  = co.alphaToCoverageEnable
            ms.alphaToOne = co.alphaToOneEnable

            w.write("minSampleShading")
            w.write("sampleMask")
            w.write("rasterSamples")
            w.write("sampleLocations")

            w.write("alphaToCoverage")
            w.write("alphaToOne")

    def viewportScissor(self,vi):
        with self.writer.beginSub("ViewportsScissors",vi) as w:
            w.write("discardRectanglesExclusive")
            w.write("discardRectangles")
            w.write("depthNegativeOneToOne")
            with self.writer.beginSubArray("Viewports") as w:
                for vid in  range(len(vi.viewportScissors)):
                    vp = vi.viewportScissors[vid].vp
                    with self.writer.beginSub("viewport",vp) as w:
                        w.write("enabled")
                        w.write("x")
                        w.write("y")
                        w.write("width")
                        w.write("height")
                        w.write("minDepth")
                        w.write("maxDepth")
            with self.writer.beginSubArray("Scissors") as w:
                for vid in  range(len(vi.viewportScissors)):
                    sc = vi.viewportScissors[vid].scissor
                    with self.writer.beginSub("scissor",sc) as w:
                        w.write("enabled")
                        w.write("x")
                        w.write("y")
                        w.write("width")
                        w.write("height")

    def colorBlend(self,co):
        with self.writer.beginSub("colorBlend",co) as w:
            w.write(f"blendFactor")
            with self.writer.beginSubArray("Blends") as w:
                for cb in co.blends:
                    if cb.enabled:
                        with self.writer.beginSubNoAppend("blend",cb) as w:
                            w.write("enabled")
                            w.write("logicOperationEnabled")
                            w.write("writeMask")
                        with self.writer.beginSubNoAppend("colorBlend",cb.colorBlend) as w:
                            w.write("source")
                            w.write("destination")
                            w.write("operation")
                        with self.writer.beginSub("alphaBlend",cb.alphaBlend) as w:
                            w.write("source")
                            w.write("destination")
                            w.write("operation")

    def output(self):
        self.output_index = [o.resourceId for o in self.state.GetOutputTargets()]
        fb = self.vkstate.currentPass.framebuffer
        fb.framebufferSRGB = None
        fb.dither          = None
        with self.writer.beginSubTitle("OutputState") as w1:
            with self.writer.beginSub("Framebuffer",fb) as w:
                w.write("framebufferSRGB")
                w.write(f"dither")
                self.colorBlend(self.vkstate.colorBlend)
    def inputAssembly(self,ia):
        ia.restartIndex ="TODO"
        ia.provokingVertexLast ="TODO"
        with self.writer.beginSub("inputAssembly",ia) as w:
            w.write("topology")
            w.write("primitiveRestartEnable")
            w.write("restartIndex")
            w.write("provokingVertexLast")

    def input(self):
        with self.writer.beginSubTitle("InputState") as w1:
            self.vertexInput()
            self.inputAssembly(self.vkstate.inputAssembly)

    def vertexInput(self):

        #inputs: List[rd.VertexInputAttribute] = self.state.GetVertexInputs()

        vbs: List[rd.BoundVBuffer] = self.state.GetVBuffers()
        attributes = self.vkstate.vertexInput.attributes
        bindings = self.vkstate.vertexInput.bindings
        vertexBuffers = self.vkstate.vertexInput.vertexBuffers
        with self.writer.beginSubTitle("attributes") as w2:
            for atr in self.vkstate.vertexInput.attributes:
                self.writer.write_attribute(atr,bindings,vertexBuffers)

    def read(self):
        self.input()
        self.depthStencil(self.vkstate.depthStencil)
        self.rasterizer(self.vkstate.rasterizer,self.vkstate.multisample,self.vkstate.colorBlend)
        self.viewportScissor(self.vkstate.viewportScissor)
        self.output()

class Resource_Reader(Reader):
    class Shaderinfo:
        name = ""
    def __init__(self,controller,state,vkstate,writer):
        super().__init__(controller,state,vkstate,writer)
        self.Data = {}
    def reshape(self,n,d,size):
        if n == 1:
            return list(d)
        return [list(d[i*size:(i+1)*size]) for i in range(n)]
    # Unpack a tuple of the given format, from the data
    def unpack_data(self,var, data: bytes, itemSize,count):

        return []

        # We don't handle 'special' formats - typically bit-packed such as 10:10:10:2
        #if fmt.Special():
            #raise RuntimeError
            #print(f"Packed formats are not supported! {fmt.compType} ")
            #return None

        format_chars = {
            #                   012345678
            rd.CompType.UInt:  "xBHxIxxxQ",
            rd.CompType.SInt:  "xbhxixxxq",
            rd.CompType.Float: "xxexfxxxd",  # only 2, 4 and 8 are valid
        }

        format_chars[rd.CompType.UNorm] = format_chars[rd.CompType.UInt]
        format_chars[rd.CompType.UScaled] = format_chars[rd.CompType.UInt]
        format_chars[rd.CompType.SNorm] = format_chars[rd.CompType.SInt]
        format_chars[rd.CompType.SScaled] = format_chars[rd.CompType.SInt]
        if compType not in format_chars:
            print(f"Packed formats are not supported! {compType} ")
            return []

        vertex_format = '=' + str(count) + format_chars[compType][itemSize]

        if data_offset >= len(data):
            return []

        # Unpack the data
        try:
            value = struct.unpack_from(vertex_format, data, 0)
        except struct.error as ex:
            raise

        # If the format needs post-processing such as normalisation, do that now
        """
        if compType == rd.CompType.UNorm:
            divisor = float((1 << (fmt.compByteWidth*8)) - 1)
            value = tuple(float(i) / divisor for i in value)
        elif compType == rd.CompType.SNorm:
            max_neg = -(1 << (fmt.compByteWidth*8 - 1))
            divisor = -float(max_neg+1)
            value = tuple(-1.0 if (i == max_neg) else float(i / divisor) for i in value)
        elif compType == rd.CompType.UScaled or compType == rd.CompType.SScaled:
            value = tuple(float(i) for i in value)
        """
        # If the format is BGRA, swap the two components
        if BGRAOrder():
            value = tuple(value[i] for i in [2, 1, 0, 3])

        return value
    def read_resource(self,name,sres,bounded):
        resourceId = bounded.resourceId
        self.writer.write_shader_resource(name,sres)
        tex_details = self.get_texture(resourceId)
        res_details = self.get_resource(resourceId)
        self.writer.write_resource(name,resourceId,tex_details,res_details)
        if resourceId not in self.Data:
            texsave = rd.TextureSave()
            texsave.resourceId = resourceId
            texsave.mip = 0
            self.Data[resourceId] = save_texture(self.controller,texsave,f"{self.writer.file.name.replace('.','-')}-{str(resourceId)}")
            #self.Data[resourceId] =  self.controller.GetTextureData(resourceId, rd.Subresource(0, 0, 0))
    def read_sampler(self,samplerBound,id):
        res_details = self.get_resource(id)
        sampler         = self.get_sampler(id)
        self.writer.write_sampler(f"sampler-{id}",res_details,sampler,samplerBound)
    def struct_value(self,var,var_check):
        stype =  var.type
        _print(f"{stype.name}  flags {stype.flags}  pointerTypeID {stype.pointerTypeID}  elements {stype.elements} arrayByteStride {stype.arrayByteStride}  baseType {stype.baseType} rows {stype.rows} columns {stype.columns} matrixByteStride {stype.matrixByteStride} ")

        return var_check.value_recurssive()

    def read(self,var,var_check,member = False):
        self.writer.array_append(var.name)
        var.compType = rd.VarTypeCompType(var.type.baseType)
        if not member:
            v = var_check.check(var.name)
        else:
            v = var_check
        dtype = var.type.name
        arraySize  = var.type.elements
        _print(f"Read dtype {dtype} arraySize {arraySize} ")
        if dtype == "float4" or dtype == "int4" or dtype == "uint4":
            itemSize  = 4
            cols      = 4
            rows      = 1
        elif dtype == "float4x4":
            itemSize  = 4
            cols      = 4
            rows      = 4
        elif dtype == "float3" or dtype == "int3" or dtype == "uint3":
            assert var.type.elements == 1
            itemSize  = 4
            cols      = 3
            rows      = 1
        elif dtype == "float2" or dtype == "int2" or dtype == "uint2":
            itemSize  = 4
            cols      = 2
            rows      = 1
        elif dtype == "float" or dtype == "int" or dtype == "uint" or dtype == "bool":
            itemSize  = 4
            cols      = 1
            rows      = 1
        elif var.compType == 0: #TypeLess
            d =  self.struct_value(var,v)
            self.Data.update(d)
            return d
        else:
            assert False,f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Not found {dtype} {var.type.baseType} { var.compType }"

        count     = cols*rows
        size      = count*arraySize*itemSize
        if arraySize > 1:
            data = v.value_recurssive()
            self.Data.update(data)
            return data
        else:
            data = v.cols(cols).rows(rows).raw_value(count)

        var.itemSize   = itemSize
        var.cols       = cols
        var.rows       = rows
        var.arraySize  = arraySize
        var.size       = size
        var.data       = data
        #self.writer.write_constant_variable(var.name,var)
        self.Data[var.name] = var
        return data

    def const_block(self,cb,var_check):
        #self.data = self.vkstate.pushconsts
        with self.writer.beginSub(cb.name,cb) as w1:
            bindMap    = self.shader.bindpointMapping.constantBlocks[cb.bindPoint]
            cb.bindset = bindMap.bindset
            cb.bind    = bindMap.bind
            w1.write("bindPoint")
            w1.write("bindset")
            w1.write("bind")
            with self.writer.beginSubArray("field") as w0:
                for var in cb.variables:
                    self.read(var,var_check)
    def write_data(self):
        self.writer.write_data(self.Data)
    def bind_name(self,bp):
        return f"{bp.bindset}-{bp.bind}"
    def get_stage_name(self,stage):
        if stage == 0:
            return "Vertex"
        elif stage == 1:
            return "Tess_Control"
        elif stage == 2:
            return "Tess_Eval"
        elif stage == 3:
            return "Geometry"
        elif stage == 4:
            return "Fragment"
        elif stage == 5:
            return "Compute"
        else:
            assert False,"Not Found Shader Stage Name"
    def get_ubo(self, id: rd.ResourceId):
        ubos = self.glstate.uniformBuffers
        for t in ubos:
            t: rd.BufferDescription
            if t.resourceId == id:
                return t
        return None
    def get_texture(self, id: rd.ResourceId):
        texs = self.controller.GetTextures()

        for t in texs:
            t: rd.TextureDescription
            if t.resourceId == id:
                return t

        return None
    def get_sampler(self, id: rd.ResourceId):
        vkpipeline : rd.VKPipeline = self.vkstate.graphics
        assert len(vkpipeline.descriptorSets) <= 1
        descset = vkpipeline.descriptorSets[0]
        for binding in descset.bindings:
            for bind in binding.binds:
                if bind.samplerResourceId == id:
                    return bind
        assert False,f"Not found {id}"
        return None

    def get_resource(self, id: rd.ResourceId):
        resources = self.controller.GetResources()
        for r in resources:
            r: rd.ResourceDescription
            if r.resourceId == id:
                return r

        return None

    def shader_glsl(self,refl):
        sh = Resource_Reader.Shaderinfo()
        sh.name  = self.get_resource(self.shader.resourceId).name
        #disasm = self.controller.DisassembleShader(self.state.GetGraphicsPipelineObject(),refl,'GLSL')
        #print(disasm)
        return sh

    def check_shader_resource(self,stage):
        self.stage = stage
        with self.writer.beginSubTitle(self.get_stage_name(stage)) as w:
            if stage == rd.ShaderStage.Vertex:
                self.shader = self.vkstate.vertexShader
            elif stage == rd.ShaderStage.Fragment:
                self.shader = self.vkstate.fragmentShader
            refl = self.state.GetShaderReflection(stage)
            sh = self.shader_glsl(refl)
            with self.writer.beginSub("Shader",sh) as w:
                w.write("name")

            bind: rd.ShaderBindpointMapping = self.state.GetBindpointMapping(self.stage)
            with self.writer.beginSubTitle("ConstantBlocks") as w0:
                cbuf = self.state.GetConstantBuffer(self.stage, 0,0)
                for slot in range(len(refl.constantBlocks)):
                    var_check = rdtest.ConstantBufferChecker(self.controller.GetCBufferVariableContents(self.state.GetGraphicsPipelineObject(),
                                                                self.state.GetShader(self.stage), self.stage,
                                                                self.state.GetShaderEntryPoint(self.stage),slot,
                                                                cbuf.resourceId, cbuf.byteOffset, cbuf.byteSize))
                    cb = refl.constantBlocks[slot]
                    print(f"{cb.name}    ConstantBlock ")
                    if cb.name == "PushConstants":
                        cb.name  = "$Globals"

                    self.const_block(cb,var_check)

            self.BoundRes = {}
            rors = self.state.GetReadOnlyResources(self.stage)
            for ror in rors:
                for res in ror.resources:
                    if int(res.resourceId) > 0:
                        self.BoundRes[self.bind_name(ror.bindPoint)] = res
                        #print(f"Boundres {res.resourceId} {res.firstMip}  {res.firstSlice} {res.typeCast} ")
            with self.writer.beginSubTitle("ReadOnlyResources") as w0:
                for slot in range(len(refl.readOnlyResources)):
                    ror = refl.readOnlyResources[slot]
                    bounded  = self.BoundRes[self.bind_name(bind.readOnlyResources[ror.bindPoint])]
                    self.read_resource(ror.name,ror,bounded)

            with self.writer.beginSubTitle("ReadWriteResources") as w0:
                for slot in range(len(refl.readWriteResources)):
                    rwr = refl.readWriteResources[slot]
                    bounded  = self.BoundRes[self.bind_name(bind.readWriteResources[rwr.bindPoint])]
                    self.read_resource(rwr.name,rwr,bounded)


            samplers = self.state.GetSamplers(self.stage)
            with self.writer.beginSubTitle("Samplers") as w0:
                for slot in range(len(samplers)):
                    sampler = samplers[slot]
                    for res in sampler.resources:
                        if int(res.resourceId) > 0:
                            self.read_sampler(sampler,res.resourceId)

class Iter_Test(rdtest.TestCase):
    slow_test = True

    def save_texture(self, texsave: rd.TextureSave):
        if texsave.resourceId == rd.ResourceId.Null():
            return



        texsave.comp.blackPoint = 0.0
        texsave.comp.whitePoint = 1.0
        texsave.alpha = rd.AlphaMapping.BlendToCheckerboard

        filename = rdtest.get_tmp_path('texsave')
        rdtest.log.print(f"Saving image of {str(texsave.resourceId)}    {filename}")
        texsave.destType = rd.FileType.HDR
        self.controller.SaveTexture(texsave, filename + ".hdr")

        texsave.destType = rd.FileType.JPG
        self.controller.SaveTexture(texsave, filename + ".jpg")

        texsave.mip = -1
        texsave.slice.sliceIndex = -1

        texsave.destType = rd.FileType.DDS
        self.controller.SaveTexture(texsave, filename + ".dds")

    def image_save(self, action: rd.ActionDescription):
        pipe: rd.PipeState = self.controller.GetPipelineState()

        texsave = rd.TextureSave()

        for res in pipe.GetOutputTargets():
            texsave.resourceId = res.resourceId
            texsave.mip = res.firstMip
            self.save_texture(texsave)

        depth = pipe.GetDepthTarget()
        texsave.resourceId = depth.resourceId
        texsave.mip = depth.firstMip
        self.save_texture(texsave)

        rdtest.log.success('Successfully saved images at {}'.format(action.eventId))

    def check_shader(self,action: rd.ActionDescription):
        self.resource.check_shader_resource(rd.ShaderStage.Vertex)
        self.resource.check_shader_resource(rd.ShaderStage.Fragment)
        self.raster.read()
        self.resource.write_data()

    def check_state(self, action: rd.ActionDescription):

        self.check(action is not None)
        self.controller.SetFrameEvent(action.eventId, False)
        vkstate: rd.VKState = self.controller.GetVulkanPipelineState()
        pipe     = self.controller.GetPipelineState()

        self.raster     = Rasterrizer_Reader(self.controller,pipe,vkstate,self.writer)
        self.resource   = Resource_Reader(self.controller,pipe,vkstate,self.writer)
        self.input      = Input_Reader(self.controller,pipe,vkstate,self.writer)
        self.input.read(action)
        self.output     = Output_Reader(self.controller,pipe,vkstate,self.writer)
        self.output.read()
        self.check_shader(action)
        self.resource.write_data()
        self.writer.write_json()
        return

        reses = {}
        for res in self.controller.GetResources():
            res: rd.ResourceDescription
            reses[res.resourceId] = res
        print(f"Resource  {reses}")
        vkpipeline : rd.VKPipeline = vkstate.graphics
        print(f"descriptorSets  { len(vkpipeline.descriptorSets) }")
        for setidx in range(len(vkpipeline.descriptorSets)):
            descset = vkpipeline.descriptorSets[setidx]
            print(f"bindings  { len(descset.bindings) }")
            for bindidx in range(len(descset.bindings)):
                binding = descset.bindings[bindidx]
                print(f"binding  firstindex {binding.firstUsedIndex} lastUsedIndex {binding.lastUsedIndex}")
                for attrID in range(len(binding.binds)):
                    attr = binding.binds[attrID]
                    print(f"Attr  offset {attr.byteOffset}  size {attr.byteSize}")
                    sampler     = reses.get(attr.samplerResourceId,None)
                    resres      = reses.get(attr.resourceResourceId,None)
                    if resres :
                        print(f"resname  {resres.name} ")
                        data = self.controller.GetBufferData(resres.resourceId, 0, 0)
                        #print(f"Data {data} ")
                        #uints = struct.unpack_from('=4L', self.controller.GetBufferData(bufin, 0, 0), 0)

    def vert_debug(self, action: rd.ActionDescription):
        pipe: rd.PipeState = self.controller.GetPipelineState()

        refl: rd.ShaderReflection = pipe.GetShaderReflection(rd.ShaderStage.Vertex)

        if pipe.GetShader(rd.ShaderStage.Vertex) == rd.ResourceId.Null():
            rdtest.log.print("No vertex shader bound at {}".format(action.eventId))
            return

        if not (action.flags & rd.ActionFlags.Drawcall):
            rdtest.log.print("{} is not a debuggable action".format(action.eventId))
            return

        vtx = int(random.random()*action.numIndices)
        inst = 0
        idx = vtx

        if action.numIndices == 0:
            rdtest.log.print("Empty action (0 vertices), skipping")
            return

        if action.flags & rd.ActionFlags.Instanced:
            inst = int(random.random()*action.numInstances)
            if action.numInstances == 0:
                rdtest.log.print("Empty action (0 instances), skipping")
                return

        if action.flags & rd.ActionFlags.Indexed:
            ib = pipe.GetIBuffer()

            mesh = rd.MeshFormat()
            mesh.indexResourceId = ib.resourceId
            mesh.indexByteStride = ib.byteStride
            mesh.indexByteOffset = ib.byteOffset + action.indexOffset * ib.byteStride
            mesh.indexByteSize = ib.byteSize
            mesh.baseVertex = action.baseVertex

            indices = rdtest.fetch_indices(self.controller, action, mesh, 0, vtx, 1)

            if len(indices) < 1:
                rdtest.log.print("No index buffer, skipping")
                return

            idx = indices[0]

            striprestart_index = pipe.GetRestartIndex() & ((1 << (ib.byteStride*8)) - 1)

            if pipe.IsRestartEnabled() and idx == striprestart_index:
                return

        rdtest.log.print("Debugging vtx %d idx %d (inst %d)" % (vtx, idx, inst))

        postvs = self.get_postvs(action, rd.MeshDataStage.VSOut, first_index=vtx, num_indices=1, instance=inst)

        trace: rd.ShaderDebugTrace = self.controller.DebugVertex(vtx, inst, idx, 0)

        if trace.debugger is None:
            self.controller.FreeTrace(trace)

            rdtest.log.print("No debug result")
            return

        cycles, variables = self.process_trace(trace)

        outputs = 0

        for var in trace.sourceVars:
            var: rd.SourceVariableMapping
            if var.variables[0].type == rd.DebugVariableType.Variable and var.signatureIndex >= 0:
                name = var.name

                if name not in postvs[0].keys():
                    raise rdtest.TestFailureException("Don't have expected output for {}".format(name))

                expect = postvs[0][name]
                value = self.evaluate_source_var(var, variables)

                if len(expect) != value.columns:
                    raise rdtest.TestFailureException(
                        "Output {} at EID {} has different size ({} values) to expectation ({} values)"
                            .format(name, action.eventId, value.columns, len(expect)))

                compType = rd.VarTypeCompType(value.type)
                if compType == rd.CompType.UInt:
                    debugged = list(value.value.u32v[0:value.columns])
                elif compType == rd.CompType.SInt:
                    debugged = list(value.value.s32v[0:value.columns])
                else:
                    debugged = list(value.value.f32v[0:value.columns])

                # For now, ignore debugged values that are uninitialised. This is an application bug but it causes false
                # reports of problems
                for comp in range(4):
                    if value.value.u32v[comp] == 0xcccccccc:
                        debugged[comp] = expect[comp]

                # Unfortunately we can't ever trust that we should get back a matching results, because some shaders
                # rely on undefined/inaccurate maths that we don't emulate.
                # So the best we can do is log an error for manual verification
                is_eq, diff_amt = rdtest.value_compare_diff(expect, debugged, eps=5.0E-06)
                if not is_eq:
                    rdtest.log.error(
                        "Debugged value {} at EID {} vert {} (idx {}) instance {}: {} difference. {} doesn't exactly match postvs output {}".format(
                            name, action.eventId, vtx, idx, inst, diff_amt, debugged, expect))

                outputs = outputs + 1

        rdtest.log.success('Successfully debugged vertex in {} cycles, {}/{} outputs match'
                           .format(cycles, outputs, len(refl.outputSignature)))

        self.controller.FreeTrace(trace)

    def pixel_debug(self, action: rd.ActionDescription):
        pipe: rd.PipeState = self.controller.GetPipelineState()

        if pipe.GetShader(rd.ShaderStage.Pixel) == rd.ResourceId.Null():
            rdtest.log.print("No pixel shader bound at {}".format(action.eventId))
            return

        if len(pipe.GetOutputTargets()) == 0 and pipe.GetDepthTarget().resourceId == rd.ResourceId.Null():
            rdtest.log.print("No render targets bound at {}".format(action.eventId))
            return

        if not (action.flags & rd.ActionFlags.Drawcall):
            rdtest.log.print("{} is not a debuggable action".format(action.eventId))
            return

        viewport = pipe.GetViewport(0)

        # TODO, query for some pixel this action actually touched.
        x = int(random.random()*viewport.width + viewport.x)
        y = int(random.random()*viewport.height + viewport.y)

        target = rd.ResourceId.Null()

        if len(pipe.GetOutputTargets()) > 0:
            valid_targets = [o.resourceId for o in pipe.GetOutputTargets() if o.resourceId != rd.ResourceId.Null()]
            rdtest.log.print("Valid targets at {} are {}".format(action.eventId, valid_targets))
            if len(valid_targets) > 0:
                target = valid_targets[int(random.random()*len(valid_targets))]

        if target == rd.ResourceId.Null():
            target = pipe.GetDepthTarget().resourceId

        if target == rd.ResourceId.Null():
            rdtest.log.print("No targets bound! Can't fetch history at {}".format(action.eventId))
            return

        rdtest.log.print("Fetching history for %d,%d on target %s" % (x, y, str(target)))

        history = self.controller.PixelHistory(target, x, y, rd.Subresource(0, 0, 0), rd.CompType.Typeless)

        rdtest.log.success("Pixel %d,%d has %d history events" % (x, y, len(history)))

        lastmod: rd.PixelModification = None

        for i in reversed(range(len(history))):
            mod = history[i]
            action = self.find_action('', mod.eventId)

            if action is None or not (action.flags & rd.ActionFlags.Drawcall):
                continue

            rdtest.log.print("  hit %d at %d (%s)" % (i, mod.eventId, str(action.flags)))

            lastmod = history[i]

            rdtest.log.print("Got a hit on a action at event %d" % lastmod.eventId)

            if mod.sampleMasked or mod.backfaceCulled or mod.depthClipped or mod.viewClipped or mod.scissorClipped or mod.shaderDiscarded or mod.depthTestFailed or mod.stencilTestFailed:
                rdtest.log.print("This hit failed, looking for one that passed....")
                lastmod = None
                continue

            if not mod.shaderOut.IsValid():
                rdtest.log.print("This hit's shader out is not valid, looking for one that valid....")
                lastmod = None
                continue

            break

        if target == pipe.GetDepthTarget().resourceId:
            rdtest.log.print("Not doing pixel debug for depth output")
            return

        if lastmod is not None:
            rdtest.log.print("Debugging pixel {},{} @ {}, primitive {}".format(x, y, lastmod.eventId, lastmod.primitiveID))
            self.controller.SetFrameEvent(lastmod.eventId, True)

            pipe: rd.PipeState = self.controller.GetPipelineState()

            trace = self.controller.DebugPixel(x, y, 0, lastmod.primitiveID)

            if trace.debugger is None:
                self.controller.FreeTrace(trace)

                rdtest.log.print("No debug result")
                return

            cycles, variables = self.process_trace(trace)

            output_index = [o.resourceId for o in pipe.GetOutputTargets()].index(target)

            if action.outputs[0] == rd.ResourceId.Null():
                rdtest.log.success('Successfully debugged pixel in {} cycles, skipping result check due to no output'.format(cycles))
                self.controller.FreeTrace(trace)
            elif (action.flags & rd.ActionFlags.Instanced) and action.numInstances > 1:
                rdtest.log.success('Successfully debugged pixel in {} cycles, skipping result check due to instancing'.format(cycles))
                self.controller.FreeTrace(trace)
            elif pipe.GetColorBlends()[output_index].writeMask == 0:
                rdtest.log.success('Successfully debugged pixel in {} cycles, skipping result check due to write mask'.format(cycles))
                self.controller.FreeTrace(trace)
            else:
                rdtest.log.print("At event {} the target is index {}".format(lastmod.eventId, output_index))

                output_sourcevar = self.find_output_source_var(trace, rd.ShaderBuiltin.ColorOutput, output_index)

                if output_sourcevar is not None:
                    debugged = self.evaluate_source_var(output_sourcevar, variables)

                    self.controller.FreeTrace(trace)

                    debuggedValue = list(debugged.value.f32v[0:4])

                    # For now, ignore debugged values that are uninitialised. This is an application bug but it causes
                    # false reports of problems
                    for idx in range(4):
                        if debugged.value.u32v[idx] == 0xcccccccc:
                            debuggedValue[idx] = lastmod.shaderOut.col.floatValue[idx]

                    # Unfortunately we can't ever trust that we should get back a matching results, because some shaders
                    # rely on undefined/inaccurate maths that we don't emulate.
                    # So the best we can do is log an error for manual verification
                    is_eq, diff_amt = rdtest.value_compare_diff(lastmod.shaderOut.col.floatValue, debuggedValue, eps=5.0E-06)
                    if not is_eq:
                        rdtest.log.error(
                            "Debugged value {} at EID {} {},{}: {} difference. {} doesn't exactly match history shader output {}".format(
                                debugged.name, lastmod.eventId, x, y, diff_amt, debuggedValue, lastmod.shaderOut.col.floatValue))

                    rdtest.log.success('Successfully debugged pixel in {} cycles, result matches'.format(cycles))
                else:
                    # This could be an application error - undefined but seen in the wild
                    rdtest.log.error("At EID {} No output variable declared for index {}".format(lastmod.eventId, output_index))

            self.controller.SetFrameEvent(action.eventId, True)

    def mesh_output(self, action: rd.ActionDescription):
        self.controller.GetPostVSData(0, 0, rd.MeshDataStage.VSOut)
        self.controller.GetPostVSData(0, 0, rd.MeshDataStage.GSOut)

        rdtest.log.success('Successfully fetched mesh output')

    def drawcall_overlay(self, action: rd.ActionDescription):
        pipe = self.controller.GetPipelineState()

        if len(pipe.GetOutputTargets()) == 0 and pipe.GetDepthTarget().resourceId == rd.ResourceId.Null():
            rdtest.log.print("No render targets bound at {}".format(action.eventId))
            return

        if not (action.flags & rd.ActionFlags.Drawcall):
            rdtest.log.print("{} is not a drawcall".format(action.eventId))
            return

        tex = rd.TextureDisplay()
        tex.overlay = rd.DebugOverlay.Drawcall
        tex.resourceId = rd.ResourceId()

        col = pipe.GetOutputTargets()
        depth = pipe.GetDepthTarget()
        if len(col) > 1 and col[0].resourceId != rd.ResourceId():
            tex.resourceId = col[0].resourceId
        elif depth.resourceId != rd.ResourceId():
            tex.resourceId = depth.resourceId

        if tex.resourceId != rd.ResourceId():
            self.texout.SetTextureDisplay(tex)
            self.texout.Display()
            rdtest.log.success('Successfully did drawcall overlay')

    def iter_action(self):

        self.sdfile = self.controller.GetStructuredFile()
        self.props: rd.APIProperties = self.controller.GetAPIProperties()
        action = self.get_first_action()
        last_action = self.get_last_action()

        self.texout = self.controller.CreateOutput(rd.CreateHeadlessWindowingData(100, 100), rd.ReplayOutputType.Texture)

        while action:
            #rdtest.log.print("{}/{}".format(action.eventId, last_action.eventId))

            self.controller.SetFrameEvent(action.eventId, False)
            #rdtest.log.print(f"Set event {action.customName}")
            action_draw = self._find_action("Draw", 0, [action] )
            if action_draw:
                #rdtest.log.print(f"Set event draw {action_draw.customName}")
                self.check_state(action_draw)
            #self.image_save(action)
            #
            action = action.next

        self.texout.Shutdown()

    def run(self,dir_path,out_path):

        exist_files = os.listdir(out_path)
        for file in sorted(os.scandir(dir_path), key=lambda e: e.name.lower()):
            if '.rdc' not in file.name:
                continue
            name = file.name.replace('.rdc','.json')
            if name in exist_files:
                continue
            # Ensure we are deterministic at least from run to run by seeding with the path
            random.seed(file.name)

            self.filename = file.name

            rdtest.log.print("Opening '{}'.".format(file.name))

            try:
                self.controller = rdtest.open_capture(file.path)
            except RuntimeError as err:
                rdtest.log.print("Skipping. Can't open {}: {}".format(file.path, err))
                continue
            self.writer =  Writer(file,out_path,self.controller)
            section_name = 'Iterating {}'.format(file.name)

            #rdtest.log.begin_section(section_name)
            self.iter_action()
            #rdtest.log.end_section(section_name)
            self.controller.Shutdown()

        rdtest.log.success("Iterated all files")


def run( dir , out_path):
    test = Iter_Test()
    rdtest.set_current_test("Vulkan-blender")
    if out_path =="":
        out_path = dir
    test.run(dir,out_path)

if __name__ == "__main__":
    run("C:\\blender\\pyrenderdoc\\data\\vk","C:\\blender\\pyrenderdoc\\data\\result")
