import argparse

from . import LogicPlum


def main():
    parser = argparse.ArgumentParser(prog='logicplum',
                                     description='LogicPlum automated machine learning.')

    parser.add_argument("--project", help="Name of the project in Logicplum AutoML.")
    parser.add_argument("--description", help="Description of the project in Logicplum AutoML.")

    parser.add_argument("--train", help="Train the data in Logicplum AutoML.")
    parser.add_argument("--target", help="Target data column in Logicplum AutoML.")

    parser.add_argument("--projectid", help="Project ID in Logicplum AutoML.")

    parser.add_argument("--score", help="Score the data from Logicplum AutoML.")

    parser.add_argument("--apikey", help="API Key to authenticate Logicplum AutoML.", required=True)

    args = parser.parse_args()

    api_key = args.apikey

    if not api_key:
        raise SystemExit("API Key required to access Logicplum AutoML.")

    if args.project:
        if not args.description:
            raise SystemExit("`--description` required to create a new project in Logicplum AutoML.")

        lp_obj = LogicPlum(api_key)
        result = lp_obj.create_project(args.project, args.description)
        print(result)

    elif args.train:
        if not args.projectid:
            raise SystemExit("`--projectid` required to train the dataset in Logicplum AutoML.")
        if not args.target:
            raise SystemExit("`--target` required to train the dataset in Logicplum AutoML.")

        lp_obj = LogicPlum(api_key)
        result = lp_obj.train(args.projectid, args.train, args.target)
        print(result)

    elif args.score:
        if not args.projectid:
            raise SystemExit("`--projectid` required to score the dataset in Logicplum AutoML.")

        lp_obj = LogicPlum(api_key)
        df = lp_obj.score(args.projectid, args.score)
        print(df)

    else:
        print("Invalid Arguments. [--project/--train/--score] required.")
