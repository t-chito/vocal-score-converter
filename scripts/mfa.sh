# https://montreal-forced-aligner.readthedocs.io/en/latest/first_steps/index.html#aligning-a-speech-corpus-with-existing-pronunciation-dictionary-and-acoustic-model

CORPUS_DIRECTORY=./songs/Recreant/4mfa

# モデルなどのダウンロード
# ダウンロード済みの場合はスキップされる
echo "----- Download models -----"
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa

# 動作に必要なファイルの確認
# https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/data_validation.html
echo "----- validate files -----"
mfa validate ${CORPUS_DIRECTORY} english_us_arpa english_us_arpa --single_speaker --beam 100 --retry_beam 400 --verbose --num_jobs 1 --use_postgres --no_final_clean # --temporary_directory  ${CORPUS_DIRECTORY}/temp

# alignment の実行
# https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/alignment.html#mfa-align
# mfa align [OPTIONS] CORPUS_DIRECTORY DICTIONARY_PATH ACOUSTIC_MODEL_PATH OUTPUT_DIRECTORY
echo "----- align -----"
mfa align ${CORPUS_DIRECTORY} english_us_arpa english_us_arpa ${CORPUS_DIRECTORY}/results --single_speaker --beam 100 --retry_beam 400 --verbose --num_jobs 1 --use_postgres