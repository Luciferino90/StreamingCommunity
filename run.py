# 10.12.23 -> 31.01.24

# Class import
import Src.Api.page as Page
from Src.Api.film import main_dw_film as download_film
from Src.Api.tv import main_dw_tv as download_tv
from Src.Util.Helper.message import msg_start
from Src.Util.Helper.console import console, msg
from Src.Upload.update import main_update
from Src.Util.FFmpeg.installer import check_ffmpeg
from Src.Util.Helper.os import remove_folder

# [ main ]
def initialize():
    
    remove_folder("tmp")
    msg_start()

    try:
        main_update()
    except Exception as e:
        console.print(f"[blue]Req github [white]=> [red]Failed: {e}")

    check_ffmpeg()
    print("\n")

def display_search_results(db_title):
    for i, title in enumerate(db_title):
        console.print(f"[yellow]{i} [white]-> [green]{title['name']} [white]- [cyan]{title['type']}")

def main():

    initialize()
    domain, site_version = Page.domain_version()

    film_search = msg.ask("\n[blue]Insert word to search in all site: ").strip()
    db_title = Page.search(film_search, domain)
    display_search_results(db_title)

    if len(db_title) != 0:
        index_select = int(msg.ask("\n[blue]Index to download: "))

        if 0 <= index_select <= len(db_title) - 1:
            selected_title = db_title[index_select]

            if selected_title['type'] == "movie":
                console.print(f"[green]\nMovie select: {selected_title['name']}")
                download_film(selected_title['id'], selected_title['slug'], domain)
            else:
                console.print(f"[green]\nTv select: {selected_title['name']}")
                download_tv(selected_title['id'], selected_title['slug'], site_version, domain)

        else:
            console.print("[red]Wrong index for selection")
    else:
        console.print("[red]Cant find a single element")

    console.print("\n[red]Done")

if __name__ == '__main__':
    main()
