import argparse
import search_papers_v2 as sp
import asyncio


async def main():
    # To create parsed instance
    parser = argparse.ArgumentParser(description="Searches articles and books of a given query")
    # For mutually exclusive group  of arguments
    # action defines what action it performs
    #group  = group.add_argument("-g", "--greeting", action='store_true')
    #group  = group.add_argument("-e", "--exclaimation", action='store_true')

    parser.add_argument("--query", required=True, help="Query name, ENTER QUERY NAME IN DOUBLE INVERTED COMMAS", type=str)
    parser.add_argument("--max_page", required=True, help="Maximum number of pages to be searched", type=int)

    parser.add_argument("-p", "--prl", help="runs prl search", action="store_true")
    parser.add_argument("--gs", help="runs prl search", action="store_true")
    parser.add_argument("-ar", "--arxiv", help="runs arxiv search", action="store_true")
    parser.add_argument("-a", "--all", help="runs arxiv,prl and google scholar search", action="store_true")

    # To call parser function
    args = parser.parse_args()

    added = 0
    if args.all:
        print("Query:", args.query, "           MAX PAGE:", args.max_page)
        print("Running arxiv, prl and google scholar search")
        sp.search_prl(args.query, args.max_page)
        sp.search_gs(args.query, args.max_page)
        sp.search_arxiv(args.query, args.max_page)
    else:
        print("Query:", args.query, "           MAX PAGE:", args.max_page)
        if args.prl:
            print("Running prl")
            sp.search_prl(args.query, args.max_page)
        if args.gs:
            print("Running google scholar")
            sp.search_gs(args.query, args.max_page)
        if args.arxiv:
            print("Running arxiv")
            sp.search_arxiv(args.query, args.max_page)


if __name__ == '__main__':
    asyncio.run(main())
