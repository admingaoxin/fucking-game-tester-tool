import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.rdtest import *
import os
import random
import struct
from typing import List
import renderdoc as rd
from src.rdtest import analyse
from src.rdtest import task
import time
from varname import nameof
import pprint
import parse_rdc_gl as gl
import parse_rdc_vk as vk
import traceback
import re
GL = 0
VK = 1
ASSERT_MODE = 1
class CompareState:
    def __init__(self,gl_basedir,vk_basedir,out_path,verbose = True,warn = False):
        self.base_dir = [gl_basedir,vk_basedir]
        self.out_json = out_path
        self.verbose = verbose
        self.warn = warn
        self.fails = {}
        self.ign   = {}
        self.sucss = {}
    def Assert(self,exp,msg,val = None,ig = False):
        if ASSERT_MODE == 0:
            assert exp,msg
        else:

            if ig:
                if self.json_names[GL] not in self.ign:
                    self.ign[self.json_names[GL]] = {
                        "vk_json" : self.json_names[VK],
                        "shader" :self.shader_name_
                        }
                ign = self.ign[self.json_names[GL]]
                ign[msg] = val
                return
                #print(f" {ign} ")
            if not exp:
                if self.json_names[GL] not in self.fails:
                    self.fails[self.json_names[GL]] = {
                        "vk_json" : self.json_names[VK],
                        "shader" :self.shader_name_
                        }
                fails = self.fails[self.json_names[GL]]
                fails[msg] = val
                #print(f" {fails} ")
            else:
                if self.json_names[GL] not in self.sucss:
                    self.sucss[self.json_names[GL]] = {
                        "vk_json" : self.json_names[VK],
                        "shader" :self.shader_name_
                        }
                sucss = self.sucss[self.json_names[GL]]
                sucss[msg] = val
                #print(f" {sucss} ")
    def val_format(self,gl,vk):
        return f"GL[{gl}] VK[{vk}]"
    def write_json(self):
        import json
        def dumper(obj):
            try:
                return obj.toJSON()
            except:
                return str(obj)
        #print(f" xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx {self.fails} ")
        with open(self.out_json, 'w') as f:
            json.dump(self.fails,f,default=dumper,indent =4)
        with open(self.out_json.replace(".json","_sucs.json"), 'w') as f:
            json.dump(self.sucss,f,default=dumper,indent =4)
        with open(self.out_json.replace(".json","_ign.json"), 'w') as f:
            json.dump(self.ign,f,default=dumper,indent =4)
    def read_json(self,json_file):
        import json
        with open(json_file) as json_data:
            data = json.load(json_data)
        #pprint.pprint(data)
        return data
    def warning(self, e1,msg=None):
        if self.warn:
            print(f"Warning {msg}  {e1}")
    def checkEQ(self, e1,e2, ignore,msg,cast = None):
        val = self.val_format(e1,e2)
        if cast:
            e1 = cast(e1)
            e2 = cast(e2)
        if self.verbose:
            print(f"CheckEQ {msg} GL={e1} VK={e2}")
        if e1 != e2:
            if not ignore:
                callstack = traceback.extract_stack()
                callstack.pop()
                assertion_line = callstack[-1].line
                assert_msg     = re.sub(r'[^(]*\((.*)?\)', r'\1', assertion_line)
            else:
                assert_msg = f"Test be failed but ignored."
        else:
            assert_msg = ""
        if ASSERT_MODE == 2:
            self.Assert( e1==e2,f"{msg}\n\n{assert_msg}",val,ignore)
        else:
            self.Assert( e1==e2,f"{msg}\n",val,ignore)
    def compare_json(self,j_gl,j_vk,iter_level):
        print(f"RDC Compare Start GLfile[{j_gl}] VKfile[{j_vk}]<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.json_names = [f"{self.base_dir[GL]}{j_gl}",f"{self.base_dir[VK]}{j_vk}"]
        self.glJson = self.read_json(self.json_names[GL])
        self.vkJson = self.read_json(self.json_names[VK])
        result = self.compare(iter_level)
        self.checkEQ(result,True,False,f"Compare IterLevel {iter_level}")
        if result:
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> RDC Compare Pass GLfile[{j_gl}] VKfile[{j_vk}]")
        else:
            print(f"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx RDC Compare Pass GLfile[{j_gl}] VKfile[{j_vk}]")
    def get_props(self,*arg):
        props = []
        for j in [self.glJson,self.vkJson]:
            d = j
            for n in arg:
                d = d[n]
            props.append(d)
        return props
    def get_prop(self,Json,*arg):
        d = Json
        for n in arg:
            d = d[n]
        return  d
    def shader_name(self,ig= False):
        for stage in ["Vertex","Fragment"]:
            names  =self.get_props(stage,"Shader","name")
            glnames = names[GL].split("-")
            assert stage[:4] == glnames[2]
            glname = glnames[1]
            self.shader_name_ = glname
            vkname = "_".join(names[VK].split("_")[:-1])
            self.checkEQ(glname ,vkname,ig,f"{stage} shader name")
    def draw_call(self,ig= False):
        dc  =self.get_props("Input","DrawCall")
        props = ["is_indexed",
                "numIndices",
                "baseVertex",
                "vertexOffset",
                "numInstances",
                "instanceOffset",
                "indexOffset"
        ]
        for prop in props:
            self.checkEQ(dc[GL][prop] ,dc[VK][prop],ig,f"DrawCallComparing [{prop}]")
        ia  =self.get_props("InputState","inputAssembly")
        props = ["topology"]
        for prop in props:
            self.checkEQ(ia[GL][prop] ,ia[VK][prop],ig,f"InputAssembly [{prop}]")
        props_war = ["primitiveRestart","restartIndex","provokingVertexLast"]
        for prop in props_war:
            self.warning(ia[GL][prop],msg=f"Uncompatible property {prop} ")
    def render_targets(self,ig = False):
        fb  =self.get_props("Output","FrameBuffer")
        props = ["width",
                "height"
        ]
        for prop in props:
            self.checkEQ(fb[GL][prop] ,fb[VK][prop],ig,f"Framebuffer [{prop}]",int)
        props = ["varName",
                "varType",
                "compCount",
                "semanticName",
                "semanticIdxName",
                "semanticIndex"]
        format =["type",
                "compCount",
                "compByteWidth",
                "compType"]

        sigs  = self.get_props("Output","FrameBuffer","Signatures")
        self.checkEQ(len(sigs[GL]),len(sigs[VK]),ig, f"Rendertargets Nums",int)
        for i in range(len(sigs[GL])):
            glsig = [v for k,v in sigs[GL][i].items()][0]
            vksig = [v for k,v in sigs[VK][i].items()][0]
            for prop in props:
                self.checkEQ(glsig[prop] ,vksig[prop], ig,f"RenderTarget Signatures [{prop}]")

        atta  = self.get_props("Output","FrameBuffer","Attchments")
        self.checkEQ(len(atta[GL]),len(atta[VK]), ig,f"Attachment Nums",int)
        N = len(atta[VK]) if len(atta[GL]) > len(atta[VK]) else len(atta[GL])
        for i in range(N):
            glata = [v for k,v in atta[GL][i].items()][0]["resource_format"]
            vkata = [v for k,v in atta[VK][i].items()][0]["resource_format"]
            for prop in format:
                self.checkEQ(glata[prop] ,vkata[prop],ig, f"Attachment Format[{prop}]",int)
    def rasterizer(self,ig = False):
        ra  =self.get_props("Rasterizer")
        props1 = ["fillMode",
        "cullMode",
        "lineWidth",
        "depthBias",
        "slopeScaledDepthBias",
        ]
        for prop in props1:
            self.checkEQ(ra[GL][prop] ,ra[VK][prop],ig,f"Rasterizer [{prop}]")
        props2 = [
        ("depthClamp","depthClampEnable"),
        ("offsetClamp","depthBiasClamp")
        ]
        for (glprop,vkprop) in props2:
            self.checkEQ(ra[GL][glprop] ,ra[VK][vkprop],ig,f"Rasterizer [{glprop}] ==[{vkprop}]")

        props3  = [
            "frontCCW"
        ]
        for prop in props3:
            self.checkEQ(ra[GL][prop] ,not ra[VK][prop],ig,f"Rasterizer [{prop}]")

        glprop = [
        "programmablePointSize",
        "pointSize",
        "pointFadeThreshold",
        "pointOriginUpperLeft",
        ]
        for prop in glprop:
            self.warning(ra[GL][prop],msg=f"Uncompatible property {prop} ")

        props3 = [
        "lineRasterMode",
        "lineStippleFactor",
        "lineStipplePattern"
        ]
        for prop in props3:
            self.warning(ra[VK][prop],msg=f"Translatable property VULKAN {prop} ")
        glhint = self.get_prop(self.glJson,"Hints")
        glhint_prop =[
        "lineSmoothing",
        "polySmoothing",
        "textureCompression",
        "lineSmoothingEnabled",
        "polySmoothingEnabled"
        ]
        for prop in glhint_prop:
            self.warning(glhint[prop],msg=f"Translatable property OpenGL {prop} ")
    def multisample(self,ig = False):
        ms  =self.get_props("Multisample")
        props1 = [("multisampleEnable","multisampleEnable"),
        ("sampleShading","sampleShadingEnable"),
        ("alphaToCoverage","alphaToCoverage"),
        ("alphaToOne","alphaToOne")
        ]
        for (glprop,vkprop) in props1:
            self.checkEQ(ms[GL][glprop] ,ms[VK][vkprop],ig,f"Rasterizer [{glprop}] ==[{vkprop}]")
        if ms[GL]["sampleShading"]:
            props1 = [("minSampleShadingRate","minSampleShading"),
        ("sampleMaskValue","sampleMask")
        ]
            for (glprop,vkprop) in props1:
                self.checkEQ(ms[GL][glprop] ,ms[VK][vkprop],ig,f"Rasterizer [{glprop}] ==[{vkprop}]")
            props2 = [
                "sampleCoverage","sampleCoverageInvert","sampleCoverageValue"
            ]
            for prop in props2:
                self.warning(ms[prop],msg=f"UnCompartible property OpenGL {prop} ")
    def depthStencil(self,ig= False):
        ds   = self.get_props("DepthStencil","depthState")
        props = [("depthFunction","depthFunction"),
                 ("depthBounds","depthBoundsEnable"),
                 ("depthWrites","depthWriteEnable"),
                 ("nearBound","minDepthBounds"),
                 ("farBound","maxDepthBounds")
        ]
        self.checkEQ(ds[GL]["depthEnable"] ,ds[VK]["depthTestEnable"],ig,f"depthTestEnable")
        if ds[GL]["depthEnable"]:
            for (glprop,vkprop) in props:
                self.checkEQ(ds[GL][glprop] ,ds[VK][vkprop],ig,f"depthTest [{glprop}] <>[{vkprop}]")

        ds   = self.get_props("DepthStencil","stencilState")
        self.checkEQ(ds[GL]["stencilEnable"] ,ds[VK]["stencilTestEnable"],ig,f"stencilTestEnable")
        if ds[GL]["stencilEnable"]:
            props = ["frontFace","backFace"]
            face = ["failOperation",
                    "depthFailOperation",
                    "function",
                    "reference",
                    "compareMask",
                    "writeMask"
            ]
            for p in props:
                glface = ds[GL][p]
                vkface = ds[VK][p]
                for prop in face:
                    self.checkEQ(glface[prop] ,vkface[prop],ig,f"depthTest {p}  [{prop}]")
                self.warning(vkface["passOperation"],"Properties only in vulkan passOperation")
    def viewportScissors(self,ig= False):
        props_viewport = ["enabled","width","height","minDepth","maxDepth"]
        vps  =self.get_props("ViewportsScissors","Viewports")
        for prop in props_viewport:
            self.checkEQ(vps[GL][0]["viewport"][prop] ,vps[VK][0]["viewport"][prop],ig,f"Viewports {prop}")

        props_scissor = ["enabled","width","height","x","y"]
        vps  =self.get_props("ViewportsScissors","Scissors")
        for prop in props_scissor:
            self.checkEQ(vps[GL][0]["scissor"][prop] ,vps[VK][0]["scissor"][prop],ig,f"Scissor [{prop}]")
    def colorBlend(self,ig= False):
        cb     = self.get_props( "OutputState","Framebuffer","colorBlend")
        attaN  = len(cb[VK]["Blends"])
        blend  = {
                        "blend": {
                            "enabled": None,
                            "logicOperationEnabled": None,
                            "writeMask": None
                        },
                        "colorBlend": {
                            "source": None,
                            "destination": None,
                            "operation": None
                        },
                        "alphaBlend": {
                            "source": None,
                            "destination": None,
                            "operation": None
                        }
        }
        def trav(d,glblend,vkblend,ig):
            for k in d:
                if d[k] == None:
                    self.checkEQ(glblend[k],vkblend[k],ig, f"Attachment Format[{k}]",int)
                else:
                    if self.verbose:
                        print(f"Struct[{k}]:: ")
                    trav(d[k],glblend[k],vkblend[k],ig)
        for i in range(attaN):
            glblend = cb[GL]["Blends"][i]
            vkblend = cb[VK]["Blends"][i]
            trav(blend,glblend,vkblend,ig)
    def bind_point(self,ig = False):
        push_field = [set(),set()]
        for stage in ["Vertex","Fragment"]:
            cb     = self.get_props( stage ,"ConstantBlocks")
            if "$Globals" in cb[GL]:
                push_field[GL] = push_field[GL].union(set(cb[GL]["$Globals"]["field"]))
                push_field[VK] = push_field[VK].union(set([a.replace("pc_","") for a in cb[VK]["$Globals"]["field"]] ))
        self.checkEQ(push_field[GL],push_field[VK],ig, f"PushConstant Field")
    def compare(self,iter_level=100):
        self.shader_name(False)
        if iter_level == 0:
            return True
        self.draw_call(False)
        if iter_level == 1:
            return True
        self.render_targets(False)
        if iter_level == 2:
            return True
        self.rasterizer(False)
        if iter_level == 3:
            return True
        self.multisample(True)
        if iter_level == 4:
            return True
        self.viewportScissors(False)
        if iter_level == 5:
            return True
        self.depthStencil(False)
        if iter_level == 6:
            return True
        self.colorBlend(False)
        if iter_level == 7:
            return True
        self.bind_point(False)
        if iter_level == 8:
            return True
        return True
    def make_pair_static(self,gl_json,vk_json,parse):
        assert len(gl_json) == len(vk_json)
        l = len(gl_json)
        pairs = []
        for i in range(l):
            gl  = gl_json[i]
            n = parse(gl)
            fnd =  False
            for vk in vk_json:
                n2 = parse(vk)
                if n == n2:
                    fnd = True
                    break
            assert fnd
            vk_json.pop(vk_json.index(vk))
            pairs.append((gl,vk))
        return pairs

if __name__ == "__main__":
    parse   = False
    verbose = False
    iter_level = 100
    if parse:
        vk.run("D:\\renderdoc\\x64\\test2\\")
        gl.run("D:\\renderdoc\\x64\\test1\\")
    else:
        gl_json    = "D:\\renderdoc\\x64\\gl_json2\\"
        vk_json    = "D:\\renderdoc\\x64\\vk_json2\\"
        comp       = CompareState(gl_json,vk_json,"D:\\renderdoc\\x64\\comp\\compare220.json",verbose)
        gl_json    = os.listdir(gl_json)
        vk_json    = os.listdir(vk_json)
        parse_func = lambda file : int(file.split(".")[-2].split("_")[-1])
        for (gl,vk) in comp.make_pair_static(gl_json,vk_json,parse_func):
            comp.compare_json(gl,vk,iter_level)
        comp.write_json()
