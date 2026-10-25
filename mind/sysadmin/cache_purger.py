import sys
import importlib

class CachePurger:
	def __init__(self):
		# Standardized list of our flat root package directory namespaces
		self.target_packages = ["mind", "body", "soul", "core"]

	def purge_neptune_module_cache(self) -> str:
		"""
		Programmatically clears active internal cache keys out of local system memory.
		Dynamically checks for root packages to support fast module reloading.
		"""
		purged_modules = []
		
		# Iterate over active keys in the system module registry map table safely
		for mod_key in list(sys.modules.keys()):
			if any(mod_key.startswith(pkg) for pkg in self.target_packages):
				del sys.modules[mod_key]
				purged_modules.append(mod_key)
				
		# Force instant re-import of our primary modules to lock fresh pointers
		try:
			import mind.inspector
			import body.pipeline_compiler
			import body.comfy_dispatch
			import soul.dialog_router
			import soul.chatter.chatter_core
			import core.orchestrator

			importlib.reload(mind.inspector)
			importlib.reload(body.pipeline_compiler)
			importlib.reload(body.comfy_dispatch)
			importlib.reload(soul.dialog_router)
			importlib.reload(soul.chatter.chatter_core)
			importlib.reload(core.orchestrator)
		except Exception as e:
			return f"🔧 Cache Purge Warning: Memory wiped but reload sequence tripped: {str(e)}"

		return f"🧹 System Purge Complete: Successfully flushed {len(purged_modules)} live namespace module references out of Python memory buffers. Next transaction pass will compile completely fresh from disk hooks."

if __name__ == "__main__":
	# Allows standalone shell execution from Proxmox maintenance routines
	purger = CachePurger()
	print(purger.purge_neptune_module_cache())