class GeneralPogoException(Exception):
    """Throw an exception that moves up to the start, and reboots"""

class NoFortFoundException(Exception):
	"""When looking for forts, there could actually be none"""