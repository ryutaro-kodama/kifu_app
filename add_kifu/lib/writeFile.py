class WriteFile():
    @staticmethod
    def writeFile(path, text_list):
        with open(path, mode='w', encoding='utf-8') as f:
            f.write('\n'.join(text_list))