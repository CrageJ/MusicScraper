import asyncio
import logging

from  src.database import Database
import src.application as App
import argparse
import json

async def main():
    logging.info('Starting Music Scraper CLI...')

    parser = argparse.ArgumentParser(description='Music Scraper CLI')
    parser.add_argument('appname', type=str, help='Name of the application database')
    parser.add_argument('command', choices=['scrape', 'get_content', 'get_aggregated_content'], help='Command to execute')
    parser.add_argument('from_year', type=int, help='Start year for the data range')
    parser.add_argument('to_year', type=int, help='End year for the data range')
    parser.add_argument('top_x', type=int, help='Retrieve top x values in category')
    parser.add_argument('--aoty', action='store_true', help='Include Album of the Year')
    parser.add_argument('--bea', action='store_true', help='Include Best Ever Albums')
    parser.add_argument('--rym', action='store_true', help='Include Rate Your Music')
    parser.add_argument('--meta', action='store_true', help='Include Metacritic')
    args = parser.parse_args()
    # currently, only aoty works
    args.bea = False
    args.rym = False
    args.meta = False


    app : App.Application = App.Application(args.appname)
    await app.async_init()
    if args.command == 'scrape':
        print('Scraping Data...')
        await scrape(app,args.top_x,args.from_year,args.to_year,args.aoty,args.bea,args.rym,args.meta)
        print('Scraping Complete')
    elif args.command == 'get_content':
        print('Retrieving Content...')
        data = await get_content(app, args.from_year, args.to_year, args.top_x, args.aoty, args.bea, args.rym, args.meta)
        print('Retrieval Complete')
        fmt = json.dumps(data)
        print(fmt)
    elif args.command == 'get_aggregated_content':
        print('Retrieving Aggregated Content...')
        data = await get_aggregated_content(app, args.from_year, args.to_year, args.top_x, args.aoty, args.bea, args.rym, args.meta)
        print('Retrieval Complete')
        fmt = json.dumps(data)
        print(fmt)
    logging.info('Closing Application')



async def scrape(app: App.Application ,top_x,from_year,to_year,aoty,bea,rym,meta):
    await app.scrape_websites(top_x, from_year, to_year, aoty,bea,rym,meta)

async def get_content(app: App.Application ,from_year,to_year,top_x,aoty,bea,rym,meta):
    return await app.get_content(top_x,from_year, to_year,  aoty,bea,rym,meta)

async def get_aggregated_content(app: App.Application ,from_year,to_year,top_x,aoty,bea,rym,meta):
    return await app.get_aggregated_content(top_x,from_year, to_year,  aoty,bea,rym,meta)


if __name__ == '__main__':
    asyncio.run(main())
