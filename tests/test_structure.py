import os.path as ph

class TestStructure:
    def test_wordcount(self):
        wdct = 'src/wordcount/'
        assert ph.isdir(wdct)
        assert ph.isfile(wdct+'mapper.py')
        assert ph.isfile(wdct+'reducer.py')

    def test_sentiment(self):
        snt = 'src/sentiment/'
        assert ph.isdir(snt)
        assert ph.isfile(snt+'lexicon.py')
        assert ph.isfile(snt+'mapper.py')
        assert ph.isfile(snt+'reducer.py')

    def test_utils(self):
        uts = 'src/utils/'
        assert ph.isdir(uts)
        assert ph.isfile(uts+'data_cli.py')
        assert ph.isfile(uts+'data_ingestion.py')
        assert ph.isfile(uts+'data_preprocessor.py')
        assert ph.isfile(uts+'logging_config.py')

    def test_other_files(self):
        assert ph.isfile('src/run_pipeline.py')
        assert ph.isfile('requirements.txt')
