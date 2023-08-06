"""
Simple data object that holds some values

┌──────────────────────────────────────────────────┐
│        These components will be updated.         │
├──────────────────────────┬────────────┬──────────┤
│           Name           │  Version   │   Size   │
├──────────────────────────┼────────────┼──────────┤
│ Cloud SDK Core Libraries │ 2020.09.18 │ 15.9 MiB │
│ gcloud cli dependencies  │ 2020.09.18 │  9.6 MiB │
└──────────────────────────┴────────────┴──────────┘

311.0.0 (2020-09-22)
  Breaking Changes
    ▪ **(Assured Workloads)** Updated gcloud assured workloads list and
      gcloud assured operations list commands to use separate flags for
      organization and location.
"""
class Object():

  def __str__(self):
    text = str(self.__class__) + "{"
    for k, v in self.__dict__.items():
      text = f"{text}'{k}': '{v}', "
    text = text[0:-2] + "}"

    return text
