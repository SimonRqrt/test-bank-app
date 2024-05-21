# test-bank-app

Ce projet vise à développer une application de gestion de comptes bancaires en utilisant la programmation orientée objet. L'application gère les opérations bancaires courantes telles que la création de compte, le dépôt d'argent, le retrait d'argent, le transfert d'argent et la consultation du solde. Les fonctionnalités sont implémentées en Python et testées à l'aide de pytest. De plus, une base de données est simulée à l'aide de mock-alchemy, et un pipeline de CI/CD est mis en place avec GitHub Actions pour garantir la fiabilité du code.

## Fonctionnalités de Base
Les fonctionnalités de base de l'application sont les suivantes :

### Création de compte : 
Création d'un nouveau compte avec un solde initial.
### Dépôt d'argent : 
Ajout d'argent au solde d'un compte existant.
### Retrait d'argent : 
Retrait d'argent d'un compte existant.
### Transfert d'argent : 
Transfert d'argent entre deux comptes.
### Consultation du solde : 
Consultation du solde actuel d'un compte.
## Configuration
- bank.py : Implémentation des classes Account et Transaction.
- init_db.py : Initialisation de la connexion à la base de données.
- example_app.py : Simulation des opérations bancaires.

## Schéma de la Base de Données
La base de données est simulée avec deux tables :

Accounts Table :
- account_id (int, PK) : Identifiant unique du compte.
- balance (float) : Solde du compte.

Transactions Table :
- transaction_id (int, PK) : Identifiant unique de la transaction.
- account_id (int, FK) : Identifiant du compte associé.
- amount (float) : Montant de la transaction.
- type (str) : Type de la transaction (deposit, withdraw, transfer).
- timestamp (datetime) : Date et heure de la transaction.

## Tests avec Pytest
Les fonctionnalités de l'application sont testées à l'aide de pytest. Les tests sont organisés en fonction des opérations bancaires et des différents scénarios. Les tests nécessitant une connexion à la base de données sont marqués avec @pytest.mark.database.

## Pipeline de CI/CD avec GitHub Actions

Un pipeline de CI/CD est configuré avec GitHub Actions pour automatiser les tests à chaque modification du dépôt. Les branches principales (main et dev) sont protégées, et toute modification doit passer par une Pull Request avec succès des tests avant fusion.
