import json
import os
import glob
from typing import Set, List, Dict, Any, Optional

class InstagramAnalytics:
    """
    Analisa dados de seguidores e seguidos do Instagram a partir de arquivos JSON.
    """
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
            'searching_files': "Procurando arquivos...", 
            'files_not_found_msg': "\nErro: Arquivos não encontrados.\nPor favor, certifique-se de que 'following.json' e 'followers_*.json' estão na mesma pasta do script ou em uma subpasta.",
            'files_found_msg': "Arquivos encontrados:",
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
            'searching_files': "Searching for files...", 
            'files_not_found_msg': "\nError: Files not found.\nPlease make sure 'following.json' and 'followers_*.json' are in the same folder as the script, or in a subfolder.",
            'files_found_msg': "Files found:",
            'language_prompt': "Choose the language / Escolha o idioma:",
            'invalid_option': "Opção inválida. Por favor, tente novamente. / Invalid option. Please try again."
        }
    }

    def __init__(self, following_filepath: str, followers_filepaths: List[str], language: str = 'en'):
        self.lang = language if language in self.TEXTS else 'en'
        self.texts = self.TEXTS[self.lang]
        following_data = self._load_json(following_filepath)
        followers_data = []
        for file in followers_filepaths:
            data = self._load_json(file)
            if data:
                followers_data.extend(data)
        self.following_set = self._extract_usernames(following_data, "relationships_following")
        self.followers_set = self._extract_usernames(followers_data)

    def _load_json(self, file_path: str) -> Optional[Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"{self.texts['file_not_found_error']} {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"{self.texts['json_decode_error']} {file_path}")
            return None

    def _extract_usernames(self, data: Optional[List[Dict]], key: Optional[str] = None) -> Set[str]:
        if not data:
            return set()
        
        usernames = set()
        user_list = data.get(key, []) if key and isinstance(data, dict) else data if isinstance(data, list) else []

        for user_item in user_list:
            try:
                username = user_item['string_list_data'][0]['value']
                usernames.add(username)
            except (KeyError, IndexError, TypeError):
                try:
                    username = user_item['title']
                    usernames.add(username)
                except (KeyError, TypeError):
                    continue
        return usernames

    def get_non_followers(self) -> List[str]:
        return sorted(list(self.following_set - self.followers_set))

    def get_analytics_summary(self) -> Dict[str, int]:
        return {
            "following": len(self.following_set),
            "followers": len(self.followers_set),
            "mutual": len(self.following_set & self.followers_set),
            "not_following_you_back": len(self.followers_set - self.following_set),
            "non_followers": len(self.following_set - self.followers_set)
        }

def print_report(analytics: InstagramAnalytics):
    summary = analytics.get_analytics_summary()
    texts = analytics.texts
    
    if not summary['following'] and not summary['followers']:
        print(texts['files_not_found_msg'])
        return

    print(f"\n{texts['analysis_title']}")
    print(f"{texts['following']:<25}: {summary['following']}")
    print(f"{texts['followers']:<25}: {summary['followers']}")
    print(f"{texts['mutuals']:<25}: {summary['mutual']}")
    print(texts['separator'])
    print(f"{texts['not_following_you_back']:<25}: {summary['non_followers']}")
    print(f"{texts['you_dont_follow_back']:<25}: {summary['not_following_you_back']}")

    non_followers_list = analytics.get_non_followers()
    print(f"\n{texts['detailed_list_title']} ({len(non_followers_list)}) ---")

    if non_followers_list:
        num_columns = 3
        column_width = max(len(name) for name in non_followers_list) + 4
        
        for i in range(0, len(non_followers_list), num_columns):
            row_items = non_followers_list[i:i + num_columns]
            print("".join(f"{item:<{column_width}}" for item in row_items))
    else:
        print(texts['no_one_great_job'])


if __name__ == "__main__":
    selected_language = ''
    texts_dict = InstagramAnalytics.TEXTS
    while True:
        print(texts_dict['en']['language_prompt'])
        print("  1. English")
        print("  2. Português")
        choice = input("Enter your choice (1/2): ")
        if choice in ('1', '2'):
            selected_language = 'en' if choice == '1' else 'pt'
            break
        else:
            print(texts_dict['en']['invalid_option'])
    
    texts = InstagramAnalytics.TEXTS[selected_language]

    try:
        script_directory = os.path.dirname(os.path.realpath(__file__))
    except NameError:
        script_directory = os.getcwd()

    print(f"\n{texts['searching_files']} em '{script_directory}'...")

    following_pattern = os.path.join(script_directory, '**', 'following.json')
    followers_pattern = os.path.join(script_directory, '**', 'followers_*.json')

    path_following_list = glob.glob(following_pattern, recursive=True)
    followers_files = glob.glob(followers_pattern, recursive=True)
    
    path_following = path_following_list[0] if path_following_list else None

    if not followers_files or not path_following:
        print(texts['files_not_found_msg'])
    else:
        print(texts['files_found_msg'])
        print(f"  - {path_following}")
        for follower_file in followers_files:
            print(f"  - {follower_file}")

        analytics = InstagramAnalytics(
            following_filepath=path_following,
            followers_filepaths=followers_files,
            language=selected_language
        )
        print_report(analytics)