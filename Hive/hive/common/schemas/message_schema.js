{
  "type" : "object", 
  "properties" : {
    "action" : {"type" : "string"},
    "to" : {"type" : "string"},
    "from" : {"type" : "string"},
    "data" : {"type" : "object"},
    "machineid" : {"type" : "string"}
  },
  "required" : [ "action", "to", "from", "data", "machineid" ]
}
