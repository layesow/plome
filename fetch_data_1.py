import requests
import pandas as pd

def import_jotform_data_to_excel():
    api_key = '210c836a9974c7a935312b1ea8943c90'  # Replace with your actual JotForm API key
    formId = '222203090268952'  # Replace with the actual form ID you want to retrieve
    max_records_per_request = 500

    all_records = []
    offset = 0

    while True:
        url = f'https://reselform.jotform.com/API/form/{formId}/submissions?apiKey={api_key}&limit={max_records_per_request}&offset={offset}'
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            break

        try:
            table_data = response.json()
            content = table_data['content']

            if not content:
                break

            for entry in content:
                # Extract data from the entry
                first_name = entry['answers']['4']['answer'].get('first', '')
                last_name = entry['answers']['4']['answer'].get('last', '')
                email = entry['answers']['7']['answer']
            
                # Extract other fields as needed
                signature = entry['answers']['5'].get('answer', '')
                numero_telephone = entry['answers']['22'].get('answer', '')
                address = entry['answers'].get('8', {})
                choix_formation = entry['answers']['11']['answer'][0]
                start_date = entry['answers']['14'].get('answer', '')
                end_date = entry['answers']['15'].get('answer', '')
                nombre_heure = entry['answers'].get('24', '')
                prix_formation = entry['answers'].get('20', '')
                passage_au = entry['answers'].get('21', {}).get('answer', '')
                votre_conseiller = entry['answers'].get('18', 'Vide')
                formation = entry['answers'].get('19', [])
                audio_appel_qualite = entry['answers'].get('27', [])
                audio_suivi_formation = entry['answers'].get('28', [])
            
                # Add these fields to the entry_data dictionary
                entry_data = {
                    'submission_date': entry['created_at'],
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'signature': signature,
                    'numero_telephone': numero_telephone,
                    'address' :address,
                    'choix_formation': choix_formation,
                    'date_debut': start_date,
                    'date_fin': end_date,
                    'nombre_heure': nombre_heure,
                    'prix_formation': prix_formation,
                    'passage_au': passage_au,
                    'votre_conseiller': votre_conseiller,
                    'formation': ', '.join(formation),
                    'audio_appel_qualite': ', '.join(audio_appel_qualite),
                    'audio_suivi_formation': ', '.join(audio_suivi_formation),
                    # Add other fields here
                }
                all_records.append(entry_data)



                offset += max_records_per_request

        except ValueError as e:
            print("Error decoding JSON response:", e)
            break

    # Create a DataFrame from the collected data
    df = pd.DataFrame(all_records)

    # Save the DataFrame to an Excel file
    df.to_excel('jotform_data.xlsx', index=False)

    print("Data imported and saved to the Excel file.")

# Call the function to import and save data
import_jotform_data_to_excel()
