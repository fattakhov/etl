from pipeline import Pipeline


if __name__ == '__main__':

    pipe = Pipeline(reader_config={'type':'sqlite', 'db_name':'example.db',
                                   'table_name':'stocks'},
                    writer_config={'type':'csv', 'file_name':'stocks.csv'})
    pipe.run()
