import pandas as pd
import os

# mental health dictionary
pre = '(?<!not)(?<!no)'
anxiety = pre + '(anxiety|anxious|antsy|restlessness|concern about the future|\
dread fear|nervousness|panic|panic attacks|paranoia|worry)'
depression = '(collapse|anger|compassion|shame|depressed|escape|loneliness|\
darkness|sensitivity|lupus|autism|jealousy|paranoia|stress|postpartum|hysteria|\
asthma|narcissism|heroin|pain mood|aggression|immature|ruthless|insecurity|\
mirage|cheating|hidden|pulse|projection|sway|negative affect|affect lability|\
emotional instability|emotional stories|emotional support|aggressiveness|snappy|\
agitated|irritable mood|altered mood|mood changes|mood swing|anger|frustration|\
apathy|loss of interest|indifference|bliss|elation|euphoria|warm fuzziness|\
calmness|depressed mood|depression|down feelings|feeling low|melancholy|\
miserable|sadness|feeling empty|fussiness|hopelessness|self-confidence|stress|suicidal ideation)'
insomnia = pre + '(abnormal dreams|nightmares|vivid dreams|asthenia|disturbed sleep|insomnia\
|sleep problems|early awakening|drowsiness|energy|lassitude|listlessness|exhaustion|\
fatigue|lethargic|sluggishness|somnolence|tiredness|weariness|hypersomnia)'
addiction = pre + '(substance dependence|physical dependence|psychological dependence|\
harmful use|withdrawal state|addiction|addictive behaviour|reinforcing|rewarding|\
psychoactive substances|depressants|stimulants|alcohol and drug dependence|\
abstinent|heavy drink|drinker|alcoholism|alcohol intake|alcohol misuse|\
alcohol consumption|alcohol addiction|destroyer|trippy|alcohol dependence|\
alcoholic| risky drinking|harmful drinking|chronic alcohol use|drinking behavior|\
behavior impairment|chronic alcoholic intoxication|problem alcohol use|\
alcohol-meat|drinking for pleasure|avoidance behaviors|occupational impairment|\
marijuana addict|cocaine addict|heroin addict|cannabis addict|hallucinogen|\
opioid abuse|war on drugs|illicit use of drugs|drug affliction|narcotics abuse|\
drug cues|drug-seeking|weakening self-regulation|drug abuse vulnerability|\
drug addiction|prescription drug abuse|drug habituation|substance-induced|\
drug misuse|ecstasy|illicit drug|chronic drug problem|drug involvement|\
drug reinforcement|drug relapse|rehab|rehabilitation|nicotine|harmful smoking|\
cigarette smoking|tobacco consumption|tobacco chewing|alternative tobacco product|\
dual-tobacco use|poly-tobacco use|tobacco dependent|electric cigarette use|\
vape pens|e-pens|e-hookah and vape sticks|smokeless tobacco|hookah|cigars|\
cigarillos and little cigars|daily smoking|tobacco use disorder|quitting smoking|\
internet gaming disorders|gaming disorder|internet addiction|social media addictions|\
smartphone addiction|attention deficit disorder|problematic online gaming|\
disordered gamer|gaming craving|video game addiction|internet game disorder|\
maladaptive player game|problem internet use|pathological game use|online game genres|\
video-game exposure|game addiction|recreational game user|addictive game behaviors|\
gaming community|gain ability to challenge and dominate others|acquire status and power|\
immersion|escape real life|gambling disorder|pathological gambling|gambling harm|\
problem gambling|problematic online gambling|disordered gamblers|compulsive gambling|\
gambling craving|silent addiction|problem gambler|gambling behavior|preoccupation with gambling|\
chronic gambler|gambling addiction|gamble harm up|mounting losses|gambling-motivated crime|\
at-risk gambling|persistent gambling|recurrent gambling|gambling-related cognitive distortion|\
uncontrolled gambling|compulsive gambling|internet addiction|problematic use|\
problematic phone use|social media addiction|addictio)'

read_path = '/data1/data_clean/'
write_path = '/data1/sgd_tweets/mental_new/'

for root, dirs, files in os.walk(read_path):
    for name in files:
        file_path = os.path.join(read_path, name)
        data = pd.read_csv(file_path, low_memory=False, lineterminator="\n")
        data["full_text"] = data.full_text.str.replace(r"@[^ ]*|#[^ ]*", '').str.lower()
        data['anxiety'] = data['full_text'].str.contains(anxiety, na=False, case=False)
        data['depression'] = data['full_text'].str.contains(depression, na=False, case=False)
        data['insomnia'] = data['full_text'].str.contains(insomnia, na=False, case=False)
        data['addiction'] = data['full_text'].str.contains(addiction, na=False, case=False)
        data.loc[(data['anxiety']|data['depression']|data['insomnia']|data['addiction']),'mental'] = True
        data.loc[~(data['anxiety']|data['depression']|data['insomnia']|data['addiction']),'mental'] = False
        file_path = os.path.join(write_path, name)
        data[data['mental']].to_csv(file_path,index=False)
        
        
