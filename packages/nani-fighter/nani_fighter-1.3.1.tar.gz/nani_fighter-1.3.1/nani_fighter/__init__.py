import argparse


class REVISION_NAMES:
    THE_BEGINNING = 'the-beginning'
    THE_SECOND_VISIT = 'the-second-visit'


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('revision',
                        help='The revision of the game to run',
                        choices=[REVISION_NAMES.THE_BEGINNING, REVISION_NAMES.THE_SECOND_VISIT])

    parsed_args = parser.parse_args()

    if parsed_args.revision == REVISION_NAMES.THE_BEGINNING:
        from nani_fighter import the_beginning
        the_beginning.run()
    elif parsed_args.revision == REVISION_NAMES.THE_SECOND_VISIT:
        from nani_fighter import the_second_visit
        the_second_visit.run()
    else:
        raise Exception('Revision not available')
