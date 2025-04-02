from interface.cli_interface import CLIInterface

def main():
    # Initialize and run CLI interface
    cli = CLIInterface()
    cli.load_data('data/station_network.json', 'data/schedule_data.json')
    cli.run()

if __name__ == '__main__':
    main()