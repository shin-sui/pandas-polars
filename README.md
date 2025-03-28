# pandas-polars

pandasとpolarsの速度比較ができます。

## get started
リポジトリをクローンして、ディレクトリに移動してください。
```
git clone git@github.com:shin-sui/pandas-polars.git
cd pandas-polars
```
以下で環境変数のセットアップをしてください。
```
bash setup.sh
```
`docker`ディレクトリに移動して、下記の手順でコンテナを立ち上げてください。
```
cd docker
docker compose up -d --build
docker compose exec pandas-polars bash
```
以下で、動作の確認ができます。
```
uv run src/main.py
```
下記のようなテーブルが表示されれば問題なく動作しています。

```
                Pandas vs Polars: Performance Comparison                 
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Process          ┃ pandas time (s) ┃ polars time (s) ┃ Faster Library ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Load csv         │        0.590410 │        0.029543 │         polars │
│ Write csv        │        7.003735 │        1.559264 │         polars │
│ Describe         │        0.051302 │        0.035183 │         polars │
│ Filter           │        0.024242 │        0.003953 │         polars │
│ Remove null      │        0.121694 │        0.006666 │         polars │
│ Conversion       │        0.002217 │        0.003745 │         pandas │
│ One-hot encoding │        0.078086 │        0.029972 │         polars │
└──────────────────┴─────────────────┴─────────────────┴────────────────┘
       Ten measurements were taken and the averages were compared        
```
