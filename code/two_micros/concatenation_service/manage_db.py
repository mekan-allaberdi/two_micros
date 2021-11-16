#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from two_micros.concatenation_service.model import db


def main():
    parser = argparse.ArgumentParser(description='Database Management Utility')
    parser.add_argument('-c', '--config', help='Configuration File', default='config.ini')
    parser.add_argument('command', choices=['info', 'create', 'delete'])
    args = parser.parse_args()
    if not os.path.exists(args.config):
        exit("Not existing configuration file '%s'" % args.config)

    config = configparser.ConfigParser()
    config.read(args.config)
    db_uri = config['cs']['db_uri']
    engine = create_engine(db_uri,
                           convert_unicode=True)
    db.session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    print('Database Management Info')
    if args.command == 'info':
        print('DB URI:', config['cs']['db_uri'])
    elif args.command == 'delete':
        print('Removing Database Data and Tables')
        db.metadata.drop_all(bind=engine)
    elif args.command == 'create':
        print('Creating Database Tables')
        db.metadata.create_all(bind=engine)
    else:
        print('Unknown command: %s', args.command)

if __name__ == '__main__':
    main()
