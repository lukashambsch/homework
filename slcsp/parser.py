import csv


class SLCSPParser:
    def __init__(self, slcsp_file='slcsp.csv', zips_file='zips.csv', plans_file='plans.csv'):
        self.slcsp_file = slcsp_file
        self.zips_file = zips_file
        self.plans_file = plans_file

    def parse(self):
        self.zips = self.get_zips()
        self.plans = self.get_plans()

        with open(self.slcsp_file, 'r') as f:
            reader = csv.DictReader(f)
            slcsp = [row for row in reader]

        for plan in slcsp:
            rate_area, state = self.get_state_and_rate_area(plan['zipcode'])
            plan['rate'] = self.get_slcsp_rate(state, rate_area)

        with open(self.slcsp_file, 'w') as f:
            writer = csv.DictWriter(f, ['zipcode', 'rate'], lineterminator='\n')
            writer.writeheader()
            writer.writerows(slcsp)
            print('Finished parsing file. Output filename: {}'.format(self.slcsp_file))

    def get_zips(self):
        with open(self.zips_file, 'r') as f:
            reader = csv.DictReader(f)
            next(reader, None)
            zips = [row for row in reader]
        return zips

    def get_state_and_rate_area(self, zipcode):
        return [(z['rate_area'], z['state']) for z in self.zips if z['zipcode'] == zipcode][0]

    def get_plans(self):
        with open(self.plans_file, 'r') as f:
            reader = csv.DictReader(f)
            next(reader, None)
            plans = [row for row in reader]
        return plans

    def get_slcsp_rate(self, state, rate_area):
        silver_plans = [p['rate'] for p in self.plans
                        if p['metal_level'] == 'Silver'
                        and p['rate_area'] == rate_area
                        and p['state'] == state]
        silver_plans = list(set(silver_plans))
        silver_plans.sort()
        if len(silver_plans) > 1:
            return silver_plans[1]
        return None


if __name__ == '__main__':
    parser = SLCSPParser()
    parser.parse()
