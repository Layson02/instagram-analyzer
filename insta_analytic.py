import json
import os

class InstagramAnalytics:
    TEXTS = {
        'pt': {
            'analysis_title': "--- Análise do Instagram ---",
            'following': "Seguindo",
            'followers': "Seguidores",
            'mutuals': "Seguidores Mútuos",
            'separator': "-" * 28,
            'not_following_you_back': "Não te seguem de volta",
            'you_dont_follow_back': "Você não segue de volta",
            'detailed_list_title': "--- Lista de quem não te segue de volta",
            'no_one_great_job': "  Ninguém. Ótimo trabalho!",
            'file_not_found_error': "Erro: O arquivo não foi encontrado em:",
            'json_decode_error': "Erro: O arquivo não é um JSON válido:",
            'searching_files': "Procurando arquivos 'following.json' e 'followers_1.json'...",
            'files_not_found_msg': "\nErro: Arquivos não encontrados.\nPor favor, certifique-se de que 'following.json' e 'followers_1.json' estão na mesma pasta do script ou em uma subpasta.",
            'language_prompt': "Escolha o idioma / Choose the language:",
            'invalid_option': "Opção inválida. Por favor, tente novamente. / Invalid option. Please try again."
        },
        'en': {
            'analysis_title': "--- Instagram Analytics ---",
            'following': "Following",
            'followers': "Followers",
            'mutuals': "Mutual Followers",
            'separator': "-" * 28,
            'not_following_you_back': "Don't Follow You Back",
            'you_dont_follow_back': "You Don't Follow Back",
            'detailed_list_title': "--- List of who doesn't follow you back",
            'no_one_great_job': "  Nobody. Great job!",
            'file_not_found_error': "Error: File not found at:",
            'json_decode_error': "Error: File is not a valid JSON:",
            'searching_files': "Searching for 'following.json' and 'followers_1.json' files...",
            'files_not_found_msg': "\nError: Files not found.\nPlease make sure 'following.json' and 'followers_1.json' are in the same folder as the script, or in a subfolder.",
            'language_prompt': "Choose the language / Escolha o idioma:",
            'invalid_option': "Opção inválida. Por favor, tente novamente. / Invalid option. Please try again."
        }
    }

    def __init__(self, following_file, followers_file, language='en'):
        self.lang = language if language in self.TEXTS else 'en'
        self.texts = self.TEXTS[self.lang] 

        self.following_data = self.load_json(following_file)
        self.followers_data = self.load_json(followers_file)
        
        if self.following_data and self.followers_data:
            self.following_set = self.extract_usernames(self.following_data, "relationships_following")
            self.followers_set = self.extract_usernames(self.followers_data)
        else:
            self.following_set = set()
            self.followers_set = set()

    def load_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"{self.texts['file_not_found_error']} {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"{self.texts['json_decode_error']} {file_path}")
            return None

    def extract_usernames(self, data, key=None):
        if data is None: return set()
        usernames = set()
        user_list = data.get(key, []) if key and isinstance(data, dict) else data if isinstance(data, list) else []

        for user_item in user_list:
            username = None
            try:
                username = user_item['string_list_data'][0]['value']
            except (KeyError, IndexError):
                try:
                    username = user_item['title']
                except KeyError:
                    continue
            if username:
                usernames.add(username)
        return usernames

    def count_following(self): return len(self.following_set)
    def count_followers(self): return len(self.followers_set)
    def count_mutual_follow(self): return len(self.following_set & self.followers_set)
    def count_non_follow_back(self): return len(self.following_set - self.followers_set)
    def count_not_following_back(self): return len(self.followers_set - self.following_set)
    def list_non_follow_back(self): return sorted(list(self.following_set - self.followers_set))

    def print_analytics(self):
        if not self.following_set and not self.followers_set:
            return

        print(self.texts['analysis_title'])
        print(f"{self.texts['following']:<25}: {self.count_following()}")
        print(f"{self.texts['followers']:<25}: {self.count_followers()}")
        print(f"{self.texts['mutuals']:<25}: {self.count_mutual_follow()}")
        print(self.texts['separator'])
        print(f"{self.texts['not_following_you_back']:<25}: {self.count_non_follow_back()}")
        print(f"{self.texts['you_dont_follow_back']:<25}: {self.count_not_following_back()}")

        nao_seguem_de_volta = self.list_non_follow_back()
        print(f"\n{self.texts['detailed_list_title']} ({len(nao_seguem_de_volta)}) ---")

        if nao_seguem_de_volta:
            num_colunas = 3
            try:
                largura_coluna = max(len(nome) for nome in nao_seguem_de_volta) + 4
            except ValueError:
                largura_coluna = 20

            for i in range(0, len(nao_seguem_de_volta), num_colunas):
                itens_linha = nao_seguem_de_volta[i:i + num_colunas]
                linha_formatada = "".join(f"{item:<{largura_coluna}}" for item in itens_linha)
                print(linha_formatada)
        else:
            print(self.texts['no_one_great_job'])

def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

if __name__ == "__main__":
    selected_language = ''
    texts_dict = InstagramAnalytics.TEXTS 
    
    while True:
        print(texts_dict['en']['language_prompt']) 
        print("  1. English")
        print("  2. Português")
        choice = input("Enter your choice (1/2): ")
        
        if choice == '1':
            selected_language = 'en'
            break
        elif choice == '2':
            selected_language = 'pt'
            break
        else:
            print(texts_dict['en']['invalid_option'])
            print("-" * 20)

    texts = InstagramAnalytics.TEXTS[selected_language]
    print(f"\n{texts['searching_files']}")
    
    current_directory = os.getcwd()
    path_following = find_file("following.json", current_directory)
    path_followers = find_file("followers_1.json", current_directory)
    
    if not path_followers or not path_following:
        print(texts['files_not_found_msg'])
    else:
        print(f"Found: {path_followers}")
        print(f"Found: {path_following}\n")
        
        analytics = InstagramAnalytics(
            following_file=path_following,
            followers_file=path_followers,
            language=selected_language
        )
        analytics.print_analytics()