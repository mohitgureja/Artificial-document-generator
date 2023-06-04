from data_generator import generator
from orchestrator import helper


def orchestrate(request_data):
    # Transform data and configurations separately for different modules
    invoice_params, generator_config, renderer_config = helper.transform_input(request_data)

    # Generate fake invoice data according to the configurations
    invoice_data = generator.generate_data(invoice_params, generator_config)
    print(invoice_data)
    return invoice_data
