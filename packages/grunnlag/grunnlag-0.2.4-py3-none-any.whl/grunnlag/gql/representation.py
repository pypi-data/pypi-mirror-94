from bergen.query import DelayedGQL


GET_REPRESENTATION = DelayedGQL("""
query Representation($id: Int!){
  representation(id: $id){
    id
    name
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
mutation Representation($sample: ID!, $name: String!){
  createRepresentation(sample: $sample, name: $name){
    name
    id
    image
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
    unique
    sample {
      id
    }
  }
}
""")