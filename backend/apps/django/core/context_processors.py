from constants import names


# TODO: Remove context_processor, because there is only one view!
def constants_processor(_):
    return {
        "constants": {
            "names": names
        }
    }
