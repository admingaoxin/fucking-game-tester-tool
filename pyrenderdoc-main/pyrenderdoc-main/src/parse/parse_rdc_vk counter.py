import sys
from typing import SupportsAbs
import rdtest
import renderdoc as rd

if 'pyrenderdoc' in globals():
	raise RuntimeError("This sample should not be run within the RenderDoc UI")


actions = {}

# Define a recursive function for iterating over actions
def iterDraw(d, indent = ''):
	global actions

	# save the action by eventId
	actions[d.eventId] = d

	# Iterate over the draw's children
	for d in d.children:
		iterDraw(d, indent + '    ')


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

	def write_dict(self,k,v):
		self.curr[k] = v
	def print(self):
		pprint.pprint(self.D)
	def write_json(self):
		import json
		def dumper(obj):
			try:
				return obj.toJSON()
			except:
				#print(f"Not Serialized {obj} {type(obj)} ")
				return str(obj)
		print(f"write json   {self.out_path}/{self.file}")
		with open(f"{self.out_path}/{self.file}", 'w') as f:
			json.dump(self.D, f,default=dumper,indent =4)



out_path  = "C:\\blender\\renderdoc\\x64\\Development\\pc_counter"
rdc = "swapbuffer.rdc"

class VK_Counters:
	demos_test_name = 'VK_Simple_Triangle'

	def check_capture(self,out_path,controller):
		self.controller = controller
		writer =  Writer("test.json",out_path,controller)
		avail = self.controller.EnumerateCounters()
		wanted = [rd.GPUCounter.EventGPUDuration, rd.GPUCounter.VSInvocations, rd.GPUCounter.PSInvocations,
				  rd.GPUCounter.IAPrimitives, rd.GPUCounter.RasterizedPrimitives, rd.GPUCounter.RasterizerInvocations,
				  rd.GPUCounter.SamplesPassed]

		counters = avail #list(set(avail).intersection(set(wanted)))

		results = self.controller.FetchCounters(counters)
		descs = {}

		for c in counters:
			descs[c] = self.controller.DescribeCounter(c)

		#action = self.find_action("Draw")

		# filter to only results from the draw
		#results = [r for r in results if r.eventId == action.eventId]

		ps = samp = None

		for r in results:
			desc: rd.CounterDescription = descs[r.counter]
			unit = desc.unit
			val = 0.
			#print(f"desc.resultType {desc.resultType}")
			if desc.resultType == 1:
				if desc.resultByteWidth ==8:
					val = r.value.d
				else:
					val = r.value.f
			else:
				if desc.resultByteWidth ==8:
					val = r.value.u64
				else:
					val = r.value.u32
			msg = "Counter %d (%s):" % (c, desc.name)  + "    %s" % desc.description + "    Returns %d byte %s, representing %s    double %f   " % (desc.resultByteWidth, desc.resultType, str(val),r.value.d)
			writer.write_dict(desc.name,msg)
			"""
			if r.counter == rd.GPUCounter.EventGPUDuration:
				val = 0.0
				if desc.resultByteWidth == 8:
					val = r.value.d
				elif desc.resultByteWidth == 4:
					val = r.value.f

				# should not be smaller than 0.1 microseconds, and should not be more than 10 milliseconds
				if val < 1.0e-7 or val > 0.01:
					raise rdtest.TestFailureException("{} of draw {}s is unexpected".format(desc.name, val))
				else:
					rdtest.log.success("{} of draw {}s is expected".format(desc.name, val))
			elif (r.counter == rd.GPUCounter.IAPrimitives or r.counter == rd.GPUCounter.RasterizedPrimitives or
				  r.counter == rd.GPUCounter.RasterizerInvocations):
				val = 0
				if desc.resultByteWidth == 8:
					val = r.value.u64
				elif desc.resultByteWidth == 4:
					val = r.value.u32

				if val != 1:
					raise rdtest.TestFailureException("{} of draw {} is unexpected".format(desc.name, val))
				else:
					rdtest.log.success("{} of draw {} is expected".format(desc.name, val))
			elif r.counter == rd.GPUCounter.VSInvocations:
				val = 0
				if desc.resultByteWidth == 8:
					val = r.value.u64
				elif desc.resultByteWidth == 4:
					val = r.value.u32

				if val != 3:
					raise rdtest.TestFailureException("{} of draw {} is unexpected".format(desc.name, val))
				else:
					rdtest.log.success("{} of draw {} is expected".format(desc.name, val))
			elif r.counter == rd.GPUCounter.PSInvocations or r.counter == rd.GPUCounter.SamplesPassed:
				val = 0
				if desc.resultByteWidth == 8:
					val = r.value.u64
				elif desc.resultByteWidth == 4:
					val = r.value.u32

				if r.counter == rd.GPUCounter.PSInvocations:
					ps = val
				else:
					samp = val

				# should be around 15000 pixels, but allow for slight rasterization differences
				if val < 14500 or val > 15500:
					raise rdtest.TestFailureException("{} of draw {} is unexpected".format(desc.name, val))
				else:
					rdtest.log.success("{} of draw {} is expected".format(desc.name, val))
				"""

		writer.write_json()
		rdtest.log.success("All counters have expected values")

def sampleCode(controller):
	global actions
	writer =  Writer("test.json",out_path,controller)
	data ={}
	actions = {}
	# Iterate over all of the root actions, so we have names for each
	# eventId
	for d in controller.GetRootActions():
		iterDraw(d)

	# Enumerate the available counters
	counters = controller.EnumerateCounters()

	if not (rd.GPUCounter.SamplesPassed in counters):
		raise RuntimeError("Implementation doesn't support Samples Passed counter")

	# Now we fetch the counter data, this is a good time to batch requests of as many
	# counters as possible, the implementation handles any book keeping.
	results = controller.FetchCounters([rd.GPUCounter.SamplesPassed])

	# Get the description for the counter we want
	samplesPassedDesc = controller.DescribeCounter(rd.GPUCounter.SamplesPassed)

	# Describe each counter
	for c in counters:
		desc = controller.DescribeCounter(c)
		if desc.name not in data:
			data[desc.name] =[]
		unit = desc.unit
		data[desc.name].append(unit.Seconds)
		val = 0.
		"""
		if desc.resultType == "Float":
			if desc.resultByteWidth ==8:
				val = r.value.d
			else:
				val = r.value.f
		else:
			if desc.resultByteWidth ==8:
				val = r.value.u64
			else:
				val = r.value.u32
		"""
		msg = "Counter %d (%s):" % (c, desc.name)  + "    %s" % desc.description + "    Returns %d byte %s, representing %s" % (desc.resultByteWidth, desc.resultType, str(val))
		writer.write_dict(desc.name,msg)
	# Look in the results for any draws with 0 samples written - this is an indication
	# that if a lot of draws appear then culling could be better.
	writer.write_json()
	results = controller.FetchCounters([rd.GPUCounter.EventGPUDuration])
	for r in results:
		draw = actions[r.eventId]
		desc = controller.DescribeCounter( r.counter)
		val = 0.
		if desc.resultType == "Float":
			if desc.resultByteWidth ==8:
				val = r.value.d
			else:
				val = r.value.f
		else:
			if desc.resultByteWidth ==8:
				val = r.value.u64
			else:
				val = r.value.u32
			
		print("EID[%d]   name %s   value  %s " % (r.eventId, desc.name, str(val)) )
		# Only care about draws, not about clears and other misc events
		if not (draw.flags & rd.ActionFlags.Drawcall):
			continue

		if samplesPassedDesc.resultByteWidth == 4:
			val = r.value.u32
		else:
			val = r.value.u64

		if val == 0:
			print("EID %d '%s' had no samples pass depth/stencil test!" % (r.eventId, draw.GetName(controller.GetStructuredFile())))

def loadCapture(filename):
	# Open a capture file handle
	cap = rd.OpenCaptureFile()

	# Open a particular file - see also OpenBuffer to load from memory
	result = cap.OpenFile(filename, '', None)

	# Make sure the file opened successfully
	if result != rd.ResultCode.Succeeded:
		raise RuntimeError("Couldn't open file: " + str(result))

	# Make sure we can replay
	if not cap.LocalReplaySupport():
		raise RuntimeError("Capture cannot be replayed")

	# Initialise the replay
	result,controller = cap.OpenCapture(rd.ReplayOptions(), None)

	if result != rd.ResultCode.Succeeded:
		raise RuntimeError("Couldn't initialise replay: " + str(result))

	return cap,controller


if 'pyrenderdoc' in globals():
	pyrenderdoc.Replay().BlockInvoke(sampleCode)
else:
	rd.InitialiseReplay(rd.GlobalEnvironment(), [])
	cap,controller = loadCapture(f"{out_path}/{rdc}")
	counter = VK_Counters()
	counter.check_capture(out_path ,controller)
	#sampleCode(controller)

	controller.Shutdown()
	cap.Shutdown()

	rd.ShutdownReplay()

