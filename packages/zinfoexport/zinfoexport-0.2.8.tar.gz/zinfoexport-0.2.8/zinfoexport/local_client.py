from .client import Client

class LocalClient(Client):
    def __init__(self, parameters_file = None):
        super().__init__(parameters_file)

    def run(self):
        """
        Create export file with parameters given.
        """
        export_dataframe = self.construct_dataframe()
        if self.file_format == ".csv":
            if self.seperate_files:
                {export_dataframe[name].to_csv(f'{name}.csv', index=False) for name in export_dataframe.keys()}
            else:
                export_dataframe.to_csv(f'{self.file_name}.csv', index=False)
        elif self.file_format == ".feather":
            if self.seperate_files:
                {export_dataframe[name].to_feather(f'{name}.feather') for name in export_dataframe.keys()}
            else:
                export_dataframe.to_feather(f'{self.file_name}.feather')


if __name__ == "__main__":
    client = LocalClient("parameters")
    client.run()