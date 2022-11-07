import argparse
import json

def translate(in_file, out_file):

    nb_res = 128
    jobs = []
    profiles = []



    with open(in_file, 'r') as f:
        for l in f:
            line = []
            if l.split()[0] != ';':
                job = {'id': int(l.split()[0]), 'profile': '{}', 'res': int(l.split()[7]), 'subtime': int(l.split()[1]), 'walltime': int(l.split()[3])}
                jobs.append(job)

    final = """{"description": "This workload is part of those which have been generated to conduct the experiments described in Batsim's JSSPP article. More information about how it has been generated can be found in the article and on the Batsim Experiments github page (https://github.com/oar-team/batsim-experiments)",
    "command": "translate_submission_times.py -i 4 -w generated_workloads/2016-05-04/g5k_workload_delay_seed1_size32.json",
    "date": "2016-05-17 10:28:31.851083"}"""

    test = json.loads(final)
    job_final = {"jobs": jobs}
    test.update(job_final)



    
    with open(out_file, 'w') as f:
        json.dump(test, f)



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