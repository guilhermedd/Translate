import argparse
import json

def translate(in_file, out_file):

    nb_res = {"nb_res": 128}
    jobs = []
    profiles = []
    num_profile = 0
    answer = -1
    FLOP_INFRASTRUCTURE = 22355
    base = "{}"
    profiles = json.loads(base)

    while answer < 1 or answer > 2:
        print("Would you like to use Walltime (press 1) or runtime (press 2)?")
        answer = int(input())


    with open(in_file, 'r') as f: # file with the workload
        for l in f:
            if l.split()[0] != ';': # ignores comments
                if answer == 1 and (int(l.split()[7])  == -1 or float(l.split()[5]) == -1 or int(l.split()[0]) == -1 or int(l.split()[1]) == -1 or int(l.split()[8]) == -1) :
                    continue
                if answer != 1 and (int(l.split()[7])  == -1 or float(l.split()[5]) == -1 or int(l.split()[0]) == -1 or int(l.split()[1]) == -1 or int(l.split()[3]) == -1) :
                    continue
                jobs.append({'id': int(int(l.split()[0]) if int(l.split()[0]) != -1 else 0), 'profile': 'profile_job_{}'.format(num_profile), 'res': int(int(l.split()[7]) if int(l.split()[7]) != -1 else 0), 'subtime': int(int(l.split()[1]) if int(l.split()[1]) != -1 else 0), 'walltime': int(int(l.split()[8]) if int(l.split()[8]) != -1 else 0)} if answer == 1 else {
                            'id': int(int(l.split()[0]) if int(l.split()[0]) != -1 else 0), 'profile': 'profile_job_{}'.format(num_profile), 'res': int(int(l.split()[7]) if int(l.split()[7]) != -1 else 0), 'subtime': int(int(l.split()[1]) if int(l.split()[1]) != -1 else 0), 'walltime': int(int(l.split()[3]) if int(l.split()[3]) != -1 else 0)})

                profiles.update({'profile_job_{}'.format(num_profile): {'type': 'parallel_homogeneous', 'cpu': int(int(l.split()[7]))*float(l.split()[5])*FLOP_INFRASTRUCTURE}})
                num_profile += 1

    final = """{"description": "This workload is part of those which have been generated to conduct the experiments described in Batsim's JSSPP article. More information about how it has been generated can be found in the article and on the Batsim Experiments github page (https://github.com/oar-team/batsim-experiments). Infrastructure details: Intel Xeon E5-2698 v4 @ 2.20GHz ==> 22.355 FLOPS",
    "command": "python3 translation.py workload_file_input json_file_output",
    "date": "03-11-2022 11:30:25"}"""

    profiles_final = {"profiles": profiles}
    updated = json.loads(final)
    final_jobs = {"jobs": jobs}
    updated.update(final_jobs)
    updated.update(nb_res)
    updated.update(profiles_final)

    with open(out_file, 'w') as f: # json file
        json.dump(updated, f, indent=4)

#             "id": 0,                      -- name
#             "profile": "delay_ft.B.1",    --
#             "res": 1,                     -- resources
#             "subtime": 0.0,               -- in time
#             "walltime": 149               -- Batsim automatically stop a job that exceeds its walltime

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='File with the workload')
    parser.add_argument('json_file', help='Destiny file')
    arg = parser.parse_args() #  arg.filename = name of the file

    translate(arg.input_file, arg.json_file)

