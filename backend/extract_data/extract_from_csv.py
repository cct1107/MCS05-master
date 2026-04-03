import pandas as pd


def extract_food_gi(file_path: str) -> list[str]:
    df = pd.read_csv(file_path)
    
    docs = []
    for _, row in df.iterrows():
        text = f"""
        Food: {row['Food Name']}
        GI: {row['GI']}
        Manufacturer: {row['Food Manufacturer'] if pd.notna(row['Food Manufacturer']) else 'Not specified'}
        Category: {row['Product Category']}
        Country: {row['Country']}
        Carbohydrate Portion: {row['Carbohydrate portion (g) / Average (g)']}
        GL: {row['GL']}
        Reference: {row['Reference']}
        Subject Type: {row['Subject Type']}
        """
        docs.append(text.strip())
    return docs

