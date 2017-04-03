var RetiredForagerBee = function() {

	ForagerBee.call(this)
	this.age = 40;
	this.job = "gamble";
	this.color = "grey";
	this.canFly = false;
	
	this.treasureChest = [];

};

RetiredForagerBee.prototype = Object.create(ForagerBee.prototype);
RetiredForagerBee.prototype. constructor = RetiredForagerBee;
RetiredForagerBee.prototype.gamble = function(value) {
		this.treasureChest.push(value);
	}
RetiredForagerBee.prototype.forage = function() {
		return "I am too old, let me play cards instead";
	}

