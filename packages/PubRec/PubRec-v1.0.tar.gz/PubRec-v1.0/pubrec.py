#!/usr/bin/env python
"""
================================= PubRec =================================
Simple python module to query the ADS databases and obtain for a given 
paper (or list of papers) the number of citations and the list of authors.

This idea is inspired by filltex (https://github.com/dgerosa/filltex) 
developed by Davide Gerosa.

Usage from cmd line: python pubrec.py --list file_with_list_of_bibcodes.txt
===========================================================================
"""

from __future__ import absolute_import, print_function
import bs4 #-- BeautifulSoup for parsing html data
import sys
from tqdm import tqdm #-- to show the progress
import argparse

if sys.version_info.major>=3:
    import urllib.request as urllib
else:
    import urllib

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_citations(ads_id):
    """This function returns the number of citations to a single entry in ADS"""
    url_contents = urllib.urlopen("https://ui.adsabs.harvard.edu/abs/"+ads_id+"/metrics").read()

    soup = bs4.BeautifulSoup(url_contents, "html.parser")
    #-- select the body of the table containing the information about citations
    tbody = soup.find("tbody")
    #-- remove the second colum which contain the description
    for td in tbody.find_all("td"):
        check = td.find("i")
        if(check != None):
            td.decompose()
    #-- save table as list of lists
    table = [[td.get_text(strip=True) for td in tr.find_all("td")] 
            for tr in tbody.find_all("tr")] 
    #-- transform list in dictionary
    dictCits = dict(table)
    return dictCits


def get_authors(ads_id):
    """This function returns the authors' list of a single entry in ADS"""
    url_contents = urllib.urlopen("https://ui.adsabs.harvard.edu/abs/"+ads_id+"/abstract").read()

    web_page = bs4.BeautifulSoup(url_contents, "html.parser")
    authors = [meta["content"] for meta in web_page.find_all("meta", {"property": "article:author"})]
  
    return authors


def arguments_parser():
    """Define some useful options to use pubrec from cmd line"""
    parser = argparse.ArgumentParser(prog='PubRec')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s','--single', action='extend', nargs='+', dest='ids',
            metavar='ID', help='ID(s) of the paper(s) in ADS')
    group.add_argument('-i', '--infile', type=str, dest='infile', metavar='INFILE',
            default='example.txt', help='read a list of bibitems (one per row) from INFILE'),
    parser.add_argument('--outfile', '-o', type=str2bool, nargs='?', dest='outfile', metavar='OUTFILE',
            default=True, help='save the inforformation on a file')
    parser.add_argument('--verbose', '-v', action='count', default=0,
            help='definy the level of verbosity [%(default)s]')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    return parser


def main(ids, infile, outfile, verbose):

    #-- check for the --outfile option
    if outfile:
        of = open('log.txt', 'w')
        of.write('----------------------------\n')
        of.write('ID \t \t citations\n')
        of.write('----------------------------\n')

    #-- check for --infile option
    if infile is not None:
        with open(infile, 'r') as f:
            bibcodes = f.read().splitlines()

            print('List of bibcodes: {}'.format(bibcodes))

    #-- check for --single option
    elif ids is not None:
        bibcodes = ids

    #-- loop over all bibcodes
    tot_citations = 0
    for bib in tqdm(bibcodes):
        cit = int(get_citations(bib)['Total citations'])
        if verbose > 0:
            print('code: {}\t cits: {}'.format(bib,cit))
        if outfile:
            of.write(bib+'\t'+str(cit)+'\n')
        
        tot_citations += cit

    if outfile:
        of.write('----------------------------\n')
        of.write('Tot. cit. \t'+str(tot_citations)+'\n')
        of.write('----------------------------\n')
        of.close()

    return tot_citations

#---------------------------------------------------------------------------
if __name__ == "__main__":

    args  = arguments_parser().parse_args()
    tot_cits = main(**args.__dict__)
    print(tot_cits)