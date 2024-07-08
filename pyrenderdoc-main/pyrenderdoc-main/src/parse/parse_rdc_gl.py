import rdtest
import os
import random
import struct
from typing import List
import renderdoc as rd
from rdtest import analyse
from rdtest import task
import functools
import operator
def flatten(a):
    return functools.reduce(operator.iconcat, a, [])

import time
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

    def __init__(self,file,out_path ,controller):
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
    def write_resource_format(self,format):
        with self.beginSub("resource_format",format) as w:
            w.write("type")
            w.write("compCount")
            w.write("compByteWidth")
            w.write("compType")

    def write_attchment(self,name,at,format):
        if int(at.resourceId) == 0:
            return
        with self.beginSub(name,at) as w:
            w.write("resourceId")
            w.write("slice")
            w.write("numSlices")
            w.write("mipLevel")
            w.write("swizzle")
            w.write_resource_format(format)

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
            w.write("addressS")
            w.write("addressT")
            w.write("addressR")
            w.write("borderColor")
            w.write("compareFunction")
            w.write("seamlessCubeMap")
            w.write("maxAnisotropy")
            w.write("maxLOD")
            w.write("minLOD")
            w.write("mipLODBias")
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
    format  = {}
    def __init__(self,controller,state,glstate):
        self.controller =controller
        self.state = state
        self.glstate = glstate
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
        self.format = format_chars
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
    def get(self,field,id):
        #for im in eval(f"self.glstate.{field}()"):
        for im in eval(f"self.controller.Get{field}()"):
            if im.resourceId == id:
                return im
        return None
    def read(self,writer):
        self.writer =writer

        with self.writer.beginSubTitle("Output") as w:
            fb =  self.glstate.framebuffer.drawFBO
            vp = self.state.GetViewport(0)

            refl = self.state.GetShaderReflection(rd.ShaderStage.Fragment)
            with self.writer.beginSub("FrameBuffer",fb) as w1:
                fb.width   = vp.width
                fb.height  = vp.height

                w1.write("resourceId")
                w1.write("width")
                w1.write("height")
                _print(f"Framebuffer{fb.resourceId} W {vp.width} H {vp.height} OutputSignatures {len(refl.outputSignature)}")
                with self.writer.beginSubArray("Signatures") as w0:
                    for sig in refl.outputSignature:
                        sig: rd.SigParameter
                        if sig.systemValue == rd.ShaderBuiltin.Position:
                            vsout_pos_name = sig.varName
                            if vsout_pos_name == '':
                                vsout_pos_name = sig.semanticName
                        self.writer.write_signature(sig.varName,sig)
                        _print(f"Output signature {sig.varName} semanticName {sig.semanticName}　semanticIdxName {sig.semanticIdxName}　semanticIndex {sig.semanticIndex}　varType   {sig.varType} compCount　{sig.compCount}")

                with self.writer.beginSubArray("Attchments") as w0:
                    for index in range(len(fb.colorAttachments)):
                        im = fb.colorAttachments[index]
                        if int(im.resourceId) == 0:
                            continue
                        _im = self.get("Textures",im.resourceId)
                        assert _im,"Not Found Texture"
                        self.writer.write_attchment("ColorAttchment",im,_im.format)
                        _print(f"Color {index}   ID { im.resourceId} slice {im. slice} numSlices {im.numSlices} mipLevel  {im.mipLevel } swizzle {im.swizzle} ")
                    im =  fb.depthAttachment
                    if int(im.resourceId) != 0:
                        _im = self.get("Textures",im.resourceId)
                        assert _im,f"Not Found Texture  {im.resourceId}"
                        self.writer.write_attchment("DepthAttchment",im,_im.format)

                    im =  fb.stencilAttachment
                    if int(im.resourceId) != 0:
                        _im = self.get("Textures",im.resourceId)
                        assert _im,f"Not Found Texture  {im.resourceId}"
                        self.writer.write_attchment("StencilAttchment",im,_im.format)

class Input_Reader(Reader):
    def read(self,action,writer):
        self.writer = writer
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


                _print(f"{'IndexedDraw' if is_indexed else 'Draw'} info numIndices {action.numIndices} baseVertex {action.baseVertex}   vertexOffset {action.vertexOffset} numInstances {action.numInstances} instanceOffset {action.instanceOffset}  indexOffset {action.indexOffset} ")

            _print(f"Bufferinfo ID {ib.resourceId} size {ib.byteSize} offset {ib.byteOffset} stride {ib.byteStride} ")
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
                    _print(f"Attributes {attr.name} Rate {attr.mesh.instStepRate} size {attr.mesh.vertexByteSize}  offset {attr.mesh.vertexByteOffset} stride {attr.mesh.vertexByteStride} format {attr.mesh.format.compType.name}  bufferID {attr.mesh.vertexResourceId} ")

            first_index = min(action.vertexOffset, action.numIndices-1)
            indices = analyse.fetch_indices(self.controller, action, mesh, 0, first_index, num_indices)
            mesh.data  = analyse.decode_mesh_data(self.controller, indices, indices, attrs, 0, 0)
            with self.writer.beginSub("mesh",mesh) as w:
                w.write("data")

class Rasterrizer_Reader(Reader):
    def checkEQ(self, v1,v2):
        print(f"Check Raster state  {v1}  ")
        #super().check(expr, msg)
    def depthStencil(self):
        with self.writer.beginSubTitle("DepthStencil") as w:
            de = self.glstate.depthState
            with self.writer.beginSub("depthState",de) as w1:
                w1.write("depthEnable")
                w1.write("depthFunction")
                w1.write("depthWrites")
                w1.write("depthBounds")
                w1.write("nearBound")
                w1.write("farBound")

            st = self.glstate.stencilState
            with self.writer.beginSub("stencilState",st) as w1:
                #self.checkEQ(de.stencilTestEnable , True)
                w1.write("stencilEnable")
                for Face in ["frontFace","backFace"]:
                    with self.writer.beginSub(Face,eval(f"st.{Face}")) as w2:
                        w2.write("failOperation")
                        w2.write("depthFailOperation")
                        w2.write("function")
                        w2.write("reference")
                        w2.write("compareMask")
                        w2.write("writeMask")

    def rasterizer(self):
        ra  = self.glstate.rasterizer.state
        with self.writer.beginSub("Rasterizer",ra) as w:
            w.write("fillMode")
            w.write("cullMode")
            w.write("frontCCW")
            w.write("depthClamp")

            w.write("depthBias")
            w.write("slopeScaledDepthBias")
            w.write("offsetClamp")
            w.write("programmablePointSize")

            w.write("pointSize")
            w.write("pointFadeThreshold")
            w.write("pointOriginUpperLeft")

            w.write("lineWidth")

        with self.writer.beginSub("Multisample",ra) as w:
            w.write("multisampleEnable")
            w.write("sampleShading")
            w.write("minSampleShadingRate")
            w.write("sampleMask")
            w.write("sampleMaskValue")
            w.write("sampleCoverage")
            w.write("sampleCoverageInvert")
            w.write("sampleCoverageValue")
            w.write("alphaToCoverage")
            #co.alphaToCoverageEnable
            w.write("alphaToOne")
            #co.alphaToOneEnable

    def viewportScissor(self):
        class VS:
            discardRectanglesExclusive = 0
            discardRectangles = 0
            depthNegativeOneToOne = 0
        with self.writer.beginSub("ViewportsScissors",VS) as w:
            w.write("discardRectanglesExclusive")
            w.write("discardRectangles")
            w.write("depthNegativeOneToOne")
            #assert  len(self.glstate.rasterizer.viewports) == 1
            with self.writer.beginSubArray("Viewports") as w0:
                for vid in  range(len(self.glstate.rasterizer.viewports)):
                    vi = self.glstate.rasterizer.viewports[vid]
                    with self.writer.beginSub("viewport",vi) as w:
                        w.write("enabled")
                        w.write("width")
                        w.write("height")
                        w.write("minDepth")
                        w.write("maxDepth")
                        _print(f"Viewport {vi.enabled} x {vi.x} y {vi.y} w {vi.width} h {vi.height} mindepth {vi.minDepth} maxdepth {vi.maxDepth} ")
            with self.writer.beginSubArray("Scissors") as w0:
                #assert  len(self.glstate.rasterizer.scissors) == 1
                for sid in  range(len(self.glstate.rasterizer.scissors)):
                    vi = self.glstate.rasterizer.scissors[sid]
                    with self.writer.beginSub("scissor",vi) as w:
                        w.write("enabled")
                        w.write("x")
                        w.write("y")
                        w.write("width")
                        w.write("height")
                        _print(f"Scissor {vi.enabled} x {vi.x} y {vi.y} w {vi.width} h {vi.height}")
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
        fb = self.glstate.framebuffer
        with self.writer.beginSubTitle("OutputState") as w1:
            with self.writer.beginSub("Framebuffer",fb) as w:
                w.write("framebufferSRGB")
                w.write(f"dither")
                self.colorBlend(fb.blendState)
    def inputAssembly(self):
        vi = self.glstate.vertexInput
        with self.writer.beginSub("inputAssembly",vi) as w:
            w.write("topology") #print(f"inputAssembly {ia.topology}")
            w.write("primitiveRestart")# print(f"inputAssembly {ia.primitiveRestartEnable}")
            w.write("restartIndex")
            w.write("provokingVertexLast")
            #print(f"inputAssembly {ia.indexBuffer}")

    def input(self):
        with self.writer.beginSubTitle("InputState") as w1:
            self.vertexInput()
            self.inputAssembly()

    def vertexInput(self):

        vbs: List[rd.BoundVBuffer] = self.state.GetVBuffers()
        vao = self.glstate.vertexInput.vertexArrayObject
        attributes = self.glstate.vertexInput.attributes
        vertexBuffers = self.glstate.vertexInput.vertexBuffers
        with self.writer.beginSubTitle("attributes") as w2:
            for atr in self.glstate.vertexInput.attributes:
                with self.writer.beginSub("attr",atr) as w3:
                    _print(f"attr enabled {atr.enabled} floatCast {atr.floatCast} format {atr.format.type} compCount {atr.format.compCount} compType {atr.format.compType} genericValue {atr.genericValue} vertexBufferSlot {atr.vertexBufferSlot} byteOffset {atr.byteOffset} ")
                    w3.write("enabled")
                    vbo = vertexBuffers[atr.vertexBufferSlot]
                with self.writer.beginSub("vbo",vbo) as w3:
                    _print(f"BufferID {vbo.resourceId}  byteStride {vbo.byteStride} byteOffset  {vbo.byteOffset } instanceDivisor {vbo.instanceDivisor} ")
                    w3.write("resourceId")

    def hints(self):
        hints = self.glstate.hints
        with self.writer.beginSub("Hints",hints) as w:
            w.write("derivatives")
            w.write("lineSmoothing")
            w.write("polySmoothing")
            w.write("textureCompression")
            w.write("lineSmoothingEnabled")
            w.write("polySmoothingEnabled")

    def read(self,w):
        self.writer = w
        self.input()
        self.depthStencil()
        self.rasterizer()
        self.viewportScissor()
        self.output()
        self.hints()

class Resource_Reader(Reader):
    class Shaderinfo:
        name = ""
    def __init__(self,controller,state,glstate):
        super().__init__(controller,state,glstate)
        self.Data = {}
    def reshape(self,n,d,size):
        if n == 1:
            return list(d)
        return [list(d[i*size:(i+1)*size]) for i in range(n)]

    def struct_value(self,var,var_check):
        stype =  var.type
        _print(f"{stype.name}  flags {stype.flags}  pointerTypeID {stype.pointerTypeID}  elements {stype.elements} arrayByteStride {stype.arrayByteStride}  baseType {stype.baseType} rows {stype.rows} columns {stype.columns} matrixByteStride {stype.matrixByteStride} ")

        return var_check.value_recurssive()
    def shader_glsl(self,refl):
        sh = Resource_Reader.Shaderinfo()
        sh.name  = self.get_resource(self.shader.shaderResourceId).name
        #disasm = self.controller.DisassembleShader(self.state.GetGraphicsPipelineObject(),refl,'GLSL')
        #print(disasm)
        return sh
    def read(self,var,var_check,member = False):
        self.writer.array_append(var.name)
        var.compType = rd.VarTypeCompType(var.type.baseType)
        if not member:
            v = var_check.check(var.name)
        else:
            v = var_check
        if var.name in self.Data:
            return self.Data[var.name]
        var.compType = rd.VarTypeCompType(var.type.baseType)
        _print(f"ReadBuffer {var.name}  type {var.type.name}  array {var.type.elements} byteOffset {var.byteOffset}  bitFieldOffset {var.bitFieldOffset}")
        dtype = var.type.name
        arraySize  = var.type.elements
        if dtype == "vec4" or dtype == "ivec4" or dtype == "uvec4":
            itemSize  = 4
            cols      = 4
            rows      = 1
        elif dtype == "mat4":
            itemSize  = 4
            cols      = 4
            rows      = 4
        elif dtype == "vec2" or dtype == "ivec2" or dtype == "uvec2":
            itemSize  = 4
            cols      = 2
            rows      = 1
        elif dtype == "vec3" or dtype == "ivec3" or dtype == "uvec3":
            itemSize  = 4
            cols      = 3
            rows      = 1
            assert var.type.elements == 1
        elif dtype == "float" or dtype == "int" or dtype == "uint" or dtype == "bool":
            itemSize   = 4
            cols       = 1
            rows       = 1
        elif dtype =="struct":
            d =  self.struct_value(var,v)
            self.Data.update(d)
            return d
        else:
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Not found {dtype}")
            assert False

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
        with self.writer.beginSub(cb.name,cb) as w1:
            bindMap = self.shader.bindpointMapping.constantBlocks[cb.bindPoint]
            _print(f"{cb.name} bindset {bindMap.bindset} bind  {bindMap.bind} ")
            cb.bindset =bindMap.bindset
            cb.bind    =bindMap.bind
            w1.write("bindPoint")
            w1.write("bindset")
            w1.write("bind")
            with self.writer.beginSubArray("field") as w0:
                for var in cb.variables:
                    self.read(var,var_check)

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
        sams = self.glstate.samplers
        for t in sams:
            t: rd.SamplerDescription
            if t.resourceId == id:
                return t
        return None

    def get_resource(self, id: rd.ResourceId):
        resources = self.controller.GetResources()

        for r in resources:
            r: rd.ResourceDescription
            if r.resourceId == id:
                return r

        return None
    def res_print(self,res):
        print(f"{res.name} type {res.resType}  bindPoint {res.bindPoint}  isTexture { res.isTexture}  isReadOnly {res.isReadOnly} ")
        va  = res.variableType
        print(f"variable  {va.name}  flags {va. flags} pointerTypeID {va.pointerTypeID} elements {va.elements} arrayByteStride {va.arrayByteStride}  baseType {va.baseType} rows {va.rows} columns  {va.columns }  matrixByteStride {va.matrixByteStride}  members {len(va.members)}")
        for var in va.members:
            print(f"{var.name} byteOffset {var.byteOffset} bitFieldOffset {var.bitFieldOffset } bitFieldSize {var.bitFieldSize}  defaultValue {var.defaultValue} type {var.type}")
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

    def write_data(self):
        self.writer.write_data(self.Data)

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
    def bind_name(self,bp):
        return f"{bp.bindset}-{bp.bind}"
    def check_shader_resource(self,stage,writer):
        self.writer = writer
        self.stage = stage
        with self.writer.beginSubTitle(self.get_stage_name(stage)) as w:
            if stage == rd.ShaderStage.Vertex:
                self.shader = self.glstate.vertexShader
            elif stage == rd.ShaderStage.Fragment:
                self.shader = self.glstate.fragmentShader

            refl = self.state.GetShaderReflection(stage)
            sh = self.shader_glsl(refl)
            with self.writer.beginSub("Shader",sh) as w:
                w.write("name")
            bind: rd.ShaderBindpointMapping = self.state.GetBindpointMapping(self.stage)

            with self.writer.beginSubTitle("ConstantBlocks") as w0:
                _print(f"constantBlocks {len(refl.constantBlocks)}")

                cbuf = self.state.GetConstantBuffer(self.stage, 0,0)
                for slot in range(len(refl.constantBlocks)):
                    cb = refl.constantBlocks[slot]
                    var_check = rdtest.ConstantBufferChecker(self.controller.GetCBufferVariableContents(self.state.GetGraphicsPipelineObject(),
                                                            self.state.GetShader(self.stage), self.stage,
                                                            self.state.GetShaderEntryPoint(self.stage), slot,
                                                            cbuf.resourceId, cbuf.byteOffset, cbuf.byteSize))
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

            return

class Iter_Test(rdtest.TestCase):
    slow_test = True
    def set_write(self,file,out_path):
        self.w = Writer(file,out_path,self.controller)

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
        self.resource.check_shader_resource(rd.ShaderStage.Vertex,self.w)
        self.resource.check_shader_resource(rd.ShaderStage.Fragment,self.w)
        self.raster.read(self.w)

    def check_state(self, action: rd.ActionDescription):

        self.check(action is not None)
        self.controller.SetFrameEvent(action.eventId, False)
        glstate: rd.GLState = self.controller.GetGLPipelineState()
        pipe     = self.controller.GetPipelineState()
        self.input      = Input_Reader(self.controller,pipe,glstate)
        self.input.read(action,self.w)
        self.output     = Output_Reader(self.controller,pipe,glstate)
        self.output.read(self.w)

        self.raster     = Rasterrizer_Reader(self.controller,pipe,glstate)
        self.resource   = Resource_Reader(self.controller,pipe,glstate)
        self.check_shader(action)
        #self.w.print()
        self.resource.write_data()
        self.w.write_json()

        return

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
            action = action.next

        self.texout.Shutdown()

class Task(task.ITask):
    def __init__(self, file,out_path):
        self.file = file
        self.out_path = out_path
    def run(self):
        test = Iter_Test()
        print(f"file {os.path.dirname(self.file.path)}")
        try:
            test.controller = rdtest.open_capture(self.file.path)
        except RuntimeError as err:
            rdtest.log.print("Skipping. Can't open {}: {}".format(self.file.path, err))
            return

        test.set_write(self.file,self.out_path)
        test.iter_action()
        test.controller.Shutdown()

def run(dir_path = "D:\\renderdoc\\x64\\rdc_gl\\",out_path = ""):
    t = time.time()
    if out_path =="":
        out_path = dir_path
    rdtest.set_current_test("OpenGL-blender")
    NUM_THREADS = 1
    if NUM_THREADS > 1:
        exec_service = task.MyExecServiceV2B(NUM_THREADS)
    #rdc_gl\\" #self.get_ref_path('', extra=True)
    exist_files = os.listdir(out_path)

    for file in sorted(os.scandir(dir_path), key=lambda e: e.name.lower()):
        if '.rdc' not in file.name:
            continue
        name = file.name.replace('.rdc','.json')
        if name in exist_files:
            continue
        print(f"$$$$$$$$$$RUN$$$$$$$$ {name} ")
        if NUM_THREADS  ==1 :
            Task(file,out_path).run()
        else:
            exec_service.submit(Task(file,out_path))
    if NUM_THREADS > 1:
        print('All tasks are submitted')
        exec_service.wait_task_done()

    print('All tasks are completed')
    if NUM_THREADS > 1: exec_service.shutdown()
    print(f"TIME {time.time() -t} s")

if __name__ == "__main__":
    #run(dir_path = "D:\\renderdoc\\x64\\test1\\")
    run(dir_path = "D:\\renderdoc\\x64\\rdc_gl\\",out_path = "D:\\renderdoc\\x64\\gl_json2")
    #run(dir_path = "D:\\renderdoc\\x64\\rdc_gl\\",out_path = "D:\\renderdoc\\x64\\gl_json")
    #test = Iter_Test()
    #rdtest.set_current_test("OpenGL-blender")
    #test.run()
