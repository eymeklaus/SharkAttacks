def clean_sex_column_f(df):
    sex_mapping = {
        "N": "unknown",
        "lli": "unknown",
        ".": "unknown",
        "M x 2": "M"
    }
    
    # 2. Apply the mapping to the whole column
    df['sex'] = df['sex'].replace(sex_mapping)
    
    # 3. Use a clean logic: if it's M or F, keep it. Otherwise, 'unknown'
    def finalize_value(x):
        val = str(x).st# The function below is a more robust way to clean the "sex" column, which includes specific mappings for known messy values and a general logic to handle any other unexpected entries.
rip().lower()
        if val in ['m', 'f']:
            return val.upper()
        return 'unknown'

    # 4. Apply that logic to every row
    df['sex'] = df['sex'].apply(finalize_value)
    
    return df
# Apply it
df2 = clean_sex_column(df2)
print(df2['sex'].unique())



def clean_attack_mapping_f(x):
    # 1. Define the mapping inside or outside the function
    type_mapping = {
         "Unprovoked": "Unprovoked",
    "Provoked": "Provoked",
    "Boating": np.nan,
    "Invalid": np.nan,
    "Sea Disaster": "Unprovoked",
    "?":  np.nan,
    "Boat": np.nan,
    "Invalid ": np.nan,
    "Questionable": np.nan,
    "Unconfirmed": np.nan,
    "Unverified": np.nan,
    "Under investigation": np.nan,
    "Watercraft": np.nan,
    "unprovoked": "Unprovoked",
    "Invalid Incident": np.nan,
    "Invalid ": np.nan    
    }
    
    # 2. Handle the mapping first
    # If the text is in our dictionary, change it. If not, keep original.
    val_as_str = str(x).strip()
    if val_as_str in type_mapping:
        x = type_mapping[val_as_str]

    # 3. Standardize to Provoked/Unprovoked/Unknown
    value = str(x).strip().lower()
    if value in ['unprovoked', 'provoked']:
        return value.title()
    else:
        return 'Unknown'

# APPLY the function to the column
df2['attack_type'] = df2['attack_type'].apply(clean_attack_mapping)

print(df2['attack_type'].unique())



def clean_activities_f(df, col, n_keywords=20, top_n=10):
    # 1. Basic Clean: lowercase, strip, remove quotes
    df2[col] = df2[col].str.lower().str.strip().str.replace(r"[\"']", '', regex=True)
    
    # 2. Quick Discovery: Find most common words (5+ chars)
    all_words = re.findall(r'\w{5,}', ' '.join(df[col].astype(str)))
    common_words = [w for w, c in Counter(all_words).most_common(n_keywords)]
    print(f"Suggested keywords: {common_words}")
    
    # 3. Consolidation: Map keywords to standardized labels
    selected = ["spearfishing", "fishing", "kayaking", "wading", "surfing", "swimming", "diving", "skiing"]
    
    for val in selected:
        df.loc[df[col].str.contains(val, na=False), col] = val
        
    # 4. Filter: Remove blanks and keep only the top N most frequent
    df = df[df[col].str.strip() != '']
    top_index = df[col].value_counts().nlargest(top_n).index
    
    return df[df[col].isin(top_index)].copy()

# Usage:
df2 = clean_activities(df2, 'activity')
print(df2['activity'].unique())


def categorize_injury_f(text):
    text = str(text).lower()
    
    category_map = {
        'Lower Extremity': ['leg', 'thigh', 'calf', 'knee', 'foot', 'feet', 'ankle', 'toe'],
        'Upper Extremity': ['arm', 'hand', 'finger', 'wrist', 'elbow', 'shoulder', 'forearm'],
        'Torso': ['torso', 'chest', 'back', 'abdomen', 'trunk'],
        'Head/Neck': ['head', 'face', 'neck', 'scalp'],
        'Equipment/None': ['no injury', 'board', 'kayak', 'boat', 'propeller']
    }
    
    found_categories = []
    for category, keywords in category_map.items():
        if any(word in text for word in keywords):
            found_categories.append(category)
            
    # --- FIX: This logic must be indented to stay INSIDE the function ---
    if len(found_categories) > 1:
        return 'Multiple Categories'
    elif len(found_categories) == 1:
        return found_categories[0]
    else:
        return 'Unspecified'

# Apply the combined function to our DataFrame
# Note: Ensure you use the correct column name (likely 'injury')
df2['body_part'] = df2['injury'].apply(categorize_injury)

print(df2['body_part'].unique())


def get_continent_f(country):
    # Mapping the specific 20 countries to their continents
    continent_map = {
        'Australia': 'Oceania',
        'New Caledonia': 'Oceania',
        'French Polynesia': 'Oceania',
        'New Zealand': 'Oceania',
        'Fiji': 'Oceania',
        'USA': 'North America',
        'Mexico': 'North America',
        'Costa Rica': 'North America',
        'Cuba': 'North America',
        'Bahamas': 'North America',
        'Brazil': 'South America',
        'Ecuador': 'South America',
        'Spain': 'Europe',
        'South Africa': 'Africa',
        'Mozambique': 'Africa',
        'Egypt': 'Africa',
        'Reunion': 'Africa',
        'Philippines': 'Asia',
        'Indonesia': 'Asia',
        'Japan': 'Asia'
    }
    
    # Return the continent if found, otherwise 'Other/Unknown'
    return continent_map.get(country, 'Other/Unknown')

# Apply the function to create a new column
df2['continent'] = df2['country'].apply(get_continent)

print(df2[['country', 'continent']].drop_duplicates())