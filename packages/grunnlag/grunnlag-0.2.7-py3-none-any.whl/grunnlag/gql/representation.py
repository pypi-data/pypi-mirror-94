from bergen.query import DelayedGQL


GET_REPRESENTATION = DelayedGQL("""
query Representation($id: ID!){
  representation(id: $id){
    id
    name
    tags
    image
    store
    unique
    sample {
      id
    }
  
  }
}
""")

CREATE_REPRESENTATION = DelayedGQL("""
mutation Representation($sample: ID!, $name: String!, $tags: [String]){
  createRepresentation(sample: $sample, name: $name, tags: $tags){
    name
    id
    image
    tags
    store
    unique
  
  }
}
""")

UPDATE_REPRESENTATION = DelayedGQL("""
mutation Representation($id: ID!){
  updateRepresentation(rep: $id){
    name
    id
    image
    tags
    store
    unique
  }
}
""")


FILTER_REPRESENTATION = DelayedGQL("""
query Representation($name: String) {
  representations(name: $name) {
    id
    name
    image
    store
    tags
    unique
    sample {
      id
    }
  }
}
""")