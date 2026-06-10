# AuctionCommityTracker
software to contain and process livestock auction buyers/sellers/animals/etc.

docker container(s) will host the webservice and database that drives the livestock auction, one "server" will be where the login information is input that will gate the client connections
server will run the docker containers and restful API to access the database

TODO:
login functinality
	server will prompt for login pin/passcode
	clients must input passcode to gain access to webservice
	
Database
	buyer 
		id
		name
		address
		phone
	exhibitor 
		id
		name
		address
		club 
	sale
		id
		buyer id
		exhibitor id
		animal id
		price
	addon
		id
		exhibitor id
		amount
	animal
		id
		ear tag no.
		name
		exhibitor id
		breed
		weight
		picture
		packer
		kill plant
		
Pages
	main menu
		buyer card
			card for buyers to post in their business window
			picture of exhibitor and animal
		buyer list (1,2,3,4)##TODO:inquire further about different versions
			list of buyers
		buyer list for sale
		sale setup
		catalog
		enter weight and sale number
		check writing
		list exhibitor checks
		exhibitors
		pre-fair day information
		master list
		resale prices
		add on entry
		add on amount per exhibitor
		add on doner summery
		add on amount per exhibitor copy
		add on donor recipient
		block screen
		invoice
		sale night pack and kill
		animals by packer
		packer summary
		animals by kill plant
		killer summary
		packer pick list
		
docker containers
	rest api 
		communication between applications
	database
		holds information about buyers/sellers/animals/etc
	main applications
		functionality for all pages