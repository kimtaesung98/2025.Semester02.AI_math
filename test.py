import numpy as np
import re
from deep_translator import GoogleTranslator
import sys

# ==============================================================================
# ▼▼▼ 설정 섹션 ▼▼▼
# ==============================================================================

# 1. 원본 텍스트 파일 경로:
#    (project.ipynb의 'churchill.txt'에 해당)
#    경로의 '\'를 '\\' 또는 '/'로 변경해야 합니다.
#    예: "C:/Users/kim25/Desktop/AI_math/churchill.txt"
INPUT_FILE_PATH = r'c:\Users\xlavh\Desktop\mc_chat\eminem_rap god, not afroid, love the way you lie.txt'

# 2. 출력 파일 이름:
#    번역된 결과가 저장될 .txt 파일 이름입니다.
OUTPUT_FILE_PATH = 'generated_translated_text.txt'

# 3. 생성할 문장 수:
#    "원본" + "번역" 쌍을 몇 번 반복 생성할지 정합니다.
NUMBER_OF_SENTENCES = 5

# 4. 문장 당 단어 수:
#    (project.ipynb의 'WORDCOUNT'에 해당)
WORDS_PER_SENTENCE = 40

# ==============================================================================
# ▲▲▲ 설정 끝 ▲▲▲
# ==============================================================================

def main():
    print(f"Starting script. Reading from: {INPUT_FILE_PATH}")

    # --- 1. 파일 읽기 및 모델 학습 (project.ipynb 로직) ---
    try:
        with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as f:
            source_text = f.read()
        
        # 구두점 앞뒤로 공백을 추가하여 단어와 분리
        source_text = re.sub(r'([.,!?])', r' \1 ', source_text)
        keywords = source_text.split()
        
        if len(keywords) < 2:
            print("Error: Input file is too short to create a model.")
            return

        keylist = []
        for i in range(len(keywords) - 1):
            keylist.append((keywords[i], keywords[i + 1]))

        word_dict = {}
        for beginning, following in keylist:
            if beginning in word_dict.keys():
                word_dict[beginning].append(following)
            else:
                word_dict[beginning] = [following]
        
        print("Successfully created Markov model.")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{INPUT_FILE_PATH}'")
        print("Please check the `INPUT_FILE_PATH` variable in the script.")
        return
    except Exception as e:
        print(f"Error during model creation: {e}")
        return

    # --- 2. 번역기 및 출력 파일 초기화 ---
    try:
        translator = GoogleTranslator(source='auto', target='ko')
        print("Translator initialized (target: Korean).")
    except Exception as e:
        print(f"Error initializing translator: {e}")
        return

    print(f"Opening output file: {OUTPUT_FILE_PATH}")
    with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
        
        # --- 3. 문장 생성, 번역 및 파일 저장 (반복) ---
        print(f"Generating {NUMBER_OF_SENTENCES} sentences...")
        
        for i in range(NUMBER_OF_SENTENCES):
            print(f"Generating sentence {i+1}/{NUMBER_OF_SENTENCES}...")
            
            # (project.ipynb 로직) - 대문자로 시작하는 첫 단어 선택
            first_word = np.random.choice(keywords)
            # islower() 대신 첫 글자가 알파벳이고 대문자인지 확인 (더 안정적)
            while not (first_word[0].isalpha() and first_word[0].isupper()):
                first_word = np.random.choice(keywords)
            
            word_chain = [first_word]
            
            # (project.ipynb 로직) - 문장 생성
            try:
                for _ in range(WORDS_PER_SENTENCE - 1):
                    last_word = word_chain[-1]
                    if last_word not in word_dict:
                        # 마지막 단어가 딕셔너리에 없으면(보통 텍스트의 맨 마지막 단어)
                        # 새 단어로 다시 시작
                        print(f"  Warning: Word '{last_word}' not in dict. Restarting chain.")
                        break # 이 문장 생성을 중단하고 다음 문장으로 넘어감
                    
                    next_word = np.random.choice(word_dict[last_word])
                    word_chain.append(next_word)
            
                # (project.ipynb 로직) - 단어 리스트를 문장으로 결합
                original_sentence = ' '.join(word_chain)
                
                # 분리했던 구두점 다시 붙이기
                original_sentence = re.sub(r' ([.,!?])', r'\1', original_sentence)

            except Exception as gen_e:
                print(f"  Error generating sentence: {gen_e}")
                continue # 다음 문장 생성 시도

            # --- 4. 번역 실행 ---
            print(f"  Translating sentence {i+1}...")
            try:
                translated_sentence = translator.translate(original_sentence)
            except Exception as trans_e:
                print(f"  Warning: Translation failed. Reason: {trans_e}")
                translated_sentence = "[번역 실패]"

            # --- 5. "원본" + "번역" 형식으로 파일에 저장 ---
            f.write("--- 원본 ---\n")
            f.write(original_sentence)
            f.write("\n\n--- 번역 ---\n")
            f.write(translated_sentence)
            f.write("\n\n" + "="*30 + "\n\n") # 문장 쌍 구분선
            
            print(f"  Done. (Sentence {i+1})")

    print("-" * 30)
    print(f"Script finished. Results saved to: {OUTPUT_FILE_PATH}")
    print("-" * 30)

if __name__ == "__main__":
    main()
