from graphql_relay.node.node import from_global_id


def input_to_dictionary(input):
    """"Method to convert Graphene inputs into dictionary"""
    dictionary = {}
    for key in input:
        # Convert GraphQL global id to database id
        # [-2:]は拡張子idの取り出し
        if key[-2:] == "id":
            input[key] = from_global_id(input[key])[1]
        dictionary[key] = input[key]
    return dictionary


# When you finish writing, update the file schema_people.py to add classes for
# the createPerson and updatePerson mutations.
