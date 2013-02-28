# ==============================================================================
# Logging
# ==============================================================================
window.LOG = (args) ->
  return if !window.console
  return if !window.console.log
  if arguments.length == 0
    return
  if arguments.length == 1
    window.console.log(arguments[0])
  else if arguments.length == 2
    window.console.log(arguments[0], arguments[1])
  else if arguments.length == 3
    window.console.log(arguments[0], arguments[1], arguments[2])
  else if arguments.length == 4
    window.console.log(arguments[0], arguments[1], arguments[2], arguments[3])
  else if arguments.length == 5
    window.console.log(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4])
  else
    window.console.log("Too many arguments to LOG function")


window.size_human = (nbytes) ->
  for suffix in ['B', 'KB', 'MB', 'GB', 'TB']
    if nbytes < 1000
      if suffix == 'B'
        return "#{nbytes} #{suffix}"
      return "#{parseInt(nbytes * 10) / 10} #{suffix}"
    nbytes /= 1024.0
