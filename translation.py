import argparse
import json

def translate(in_file, out_file):

    nb_res = {"nb_res": 128}
    jobs = []
    profiles = {"profiles": 
        {
            "simple": {
                "type": "parallel",
                "cpu": [5e6,  0,  0,  0],
                "com": [5e6,  0,  0,  0,
                        5e6,5e6,  0,  0,
                        5e6,5e6,  0,  0,
                        5e6,5e6,5e6,  0]
            },
            "homogeneous": {
                "type": "parallel_homogeneous",
                "cpu": 10e6,
                "com": 1e6
            },
            "homogeneous_no_cpu": {
                "type": "parallel_homogeneous",
                "cpu": 0,
                "com": 1e6
            },
            "homogeneous_no_com": {
                "type": "parallel_homogeneous",
                "cpu": 2e5,
                "com": 0
            },
            "sequence": {
                "type": "composed",
                "repeat" : 4,
                "seq": ["simple","homogeneous","simple"]
            },
            "delay": {
                "type": "delay",
                "delay": 20.20
            },
            "homogeneous_total": {
                "type": "parallel_homogeneous_total",
                "cpu": 10e6,
                "com": 1e6
            }
        }
    }

    with open(in_file, 'r') as f: # file with the workload
        for l in f:
            if l.split()[0] != ';': # ignores comments
                job = {'id': int(l.split()[0]), 'profile': 'parallel_homogeneous', 'res': int(l.split()[7]), 'subtime': int(l.split()[1]), 'walltime': int(l.split()[3])}
                jobs.append(job)

    final = """{"description": "This workload is part of those which have been generated to conduct the experiments described in Batsim's JSSPP article. More information about how it has been generated can be found in the article and on the Batsim Experiments github page (https://github.com/oar-team/batsim-experiments)",
    "command": "python3 translation.py workload_file_input json_file_output",
    "date": "03-11-2022 11:30:25"}"""

    test = json.loads(final)
    job_final = {"jobs": jobs}
    test.update(job_final)
    test.update(nb_res)
    test.update(profiles)

    with open(out_file, 'w') as f: # json file
        json.dump(test, f, indent=2, sort_keys=True)

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
