*** Signatures Numériques ***

** Bon à savoir **

* Le projet comporte une version de code python en mode présenté (fichiers jupyter notebooks (.ipynb) formée des codes :
	- 'Signature.ipynb' : code qui permet à l'envoyeur de signer son message
	- 'Vérification.ipynb' : code qui permet au destinataire de vérifier l'intégrité du message
	
* Le projet dispose aussi d'une version de programmes python natifs ('.py') qui sont juste des réecritures des 2 fichiers  plus haut sous forme de programme tout court.

** Comment fontionne le projet **

* L'envoyeur copie son message dans le fichier 'message.txt' qui se trouve dans le dossier 'Signature'

* Il éxecute le programme 'Signature.py', pour signer son message

* La clé privée est automatiquement stockée dans le fichier 'PrivateKey.txt'

* La clé publique et le message signé sont respectivement dans les fichiers 'PublicKey.txt' et 'SignedMessage.txt' du dossier 'Signature'

* Il suffira alors à celui qui signe d'envoyer le dossier 'Signature' au destinataire, vu qu'il contient aussi le message en clair

* Le destinataire va juste exécuter le fichier 'Vérification.py' qui lui affichera un message, qui va lui permettre de savoir si le message reçu est intègre ou pas

** A propos **

* Ce projet a été réalisé par des étudiants du 3GI ENSPY Promotion 2026, dont les noms suivent :

	- KAMDEM POUOKAM IVANN HAROLD
	- KENFACK NOUMEDEM FRANCK ULRICH
	- WADOH TCHINDA PAVEL DIOR
	- KENGNE TUEGUEM FRESNEL GRÂCE
	- BIHAY RAPHAEL

