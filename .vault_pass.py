import os
if 'VAULT_PASSWORD' in os.environ:
   print (os.environ['VAULT_PASSWORD'])
else:
   print ('')