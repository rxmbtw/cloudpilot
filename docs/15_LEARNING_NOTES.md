## 2026-10-10 — Secret leak & rotation

**Symptom:** secret.yaml and SSH private key were in public git history.
**Root cause:** secrets committed before .gitignore rules existed.
**Fix:** rotated DB password, SECRET_KEY, GitHub Secrets; deleted AWS key pair + server.
**Verification:** old password rejected, forged JWT → 401, CI fingerprints matched.
**Lessons:**
1. Deleting from git ≠ removing a leak. Rotate.
2. Postgres only reads POSTGRES_PASSWORD on first init → ALTER USER.
3. Pods read env only at startup → rollout restart.
4. EC2 keys are baked in at first boot → replace the server.
5. Prove the OLD secret fails, not just that the new one works.
**Prevention:** GitHub push protection on; never commit .env/keys.




## new AWS Account Day 2026:10:31

Enabled MFA to the root user 
as well as to IAM user with Passkey 

Set the Region to us-east-1 as default from user settings 

Insted of login using Access Keys 
logged as aws login --remote (no need to store permananet credentials on the laptop)

## Added the filter expression to the budget Using CLI through API aws budgets update-budget --account-ID --new-budget 
"FilterExpression": {
    "Not": {"Dimensions": {"Key": "RECORD_TYPE", "Values": ["Credit", "Refund"]}}
  }
 we added it for the alerts to work  because without it the alerts never gets fired becasue the budgets see the total cost which will always be 0$ because the credits cover the usage. 


-  created two budgets using the console
1 cloudpilot-monthly 
2 cloudpilot-daily-tripwire

-  Added email recipients to both the budgets then verified the mail. 

-  Alerts 

Cloudpilot-monthly = 4 Alerts (Monthly usage = 25$)
Actual cost > 50% 
Actual cost > 80%
Actual cost > 100%
Forecasted cost > 100%

Cloudpilot-daily-tripwire (Daily amount = $3)
Actual cost > 100%

##  monthly vs Daily-trip-wire 
monthly monitors the amount which is used by services thorugh an enitre month and send alerts accordingly. 
the Daily-trip-wire Tracks daily usage limit which helps user form keeping services on by mistake  and reminds to deleted whatever is created or configured wich is spiking the budgets daily limit. 

The Remote login Eliminated the need to use the credentails 
also user do no require to store or maintain them  
and prevention form unwanted access if stolen

## Cost Anomaly Detection under it 
 -Created one Cost monitor 
 -named = cloudpilot-services 
 -Attached = cloudpilot-anomaly-alerts 
 Threshold (reached or exceeded)
 $5.00

 #On billing Preferences 
 added these 
 Invoice delivery preferences 
 PDF invoices delivery by email
 

 -Added Alert Preferences 
 AWS Free Tier alerts
my email
CloudWatch billing alerts
