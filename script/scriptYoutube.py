import os
import argparse
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Declaro la clave de google developer
DEVELOPER_KEY = "AIzaSbSjj3FbVAfVUEvYPTKNjo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Función que devuelve la lista de videos del canal
def get_video_list(youtube, channel_id):
    videos = []
    next_page_token = None
    
    while True:
        # Realizar la búsqueda de videos
        search_response = youtube.search().list(
            channelId=channel_id,
            type='video',
            part='id,snippet',
            maxResults=50,  # máximo número de resultados a recuperar
            pageToken=next_page_token
        ).execute()
        
        # Recorrer los resultados de la búsqueda
        for search_result in search_response.get("items", []):
            title = search_result["snippet"]["title"]
            video_id = search_result["id"]["videoId"]
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            videos.append((video_url, title))
        
        # Si hay más páginas de resultados, continuar con la siguiente
        next_page_token = search_response.get('nextPageToken')
        if not next_page_token:
            break
    
    return videos

def main(args):
    # Crear un objeto con la API de YouTube
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    # Obtener la lista de videos
    video_list = get_video_list(youtube, args.channel_id)
    
    # Convertir la lista de videos en un objeto DataFrame de Pandas
    df = pd.DataFrame(video_list, columns=['url', 'title'])
    
    # Guardar el archivo CSV
    df.to_csv(args.output_file, index=False)
    
    # Eliminar el archivo lista.txt
    os.remove('lista.txt')

if __name__ == '__main__':
    # Definir los argumentos de línea de comandos
    parser = argparse.ArgumentParser()
    parser.add_argument('channel_id', type=str, help='ID del canal de YouTube')
    parser.add_argument('output_file', type=str, help='Ruta del archivo de salida CSV')
    args = parser.parse_args()
    
    # Ejecutar la función principal
    main(args)
