from data_generator import helper


def generate_data(params, config):
    json_data = helper.read_json("data/invoice.json")
    invoice_params = [key for key in params.keys() if params[key] is True]
    print(invoice_params)
    invoice_data = []
    for i in range(config["invoice_count"]):
        invoice_data.append({key: json_data[i][key] for key in params.keys() if params[key] is True})
    # for key in params.keys():
    #     invoice_data[key] = json_data[0][key]
    return invoice_data
