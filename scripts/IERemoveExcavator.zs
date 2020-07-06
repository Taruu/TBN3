import crafttweaker.recipes.ICraftingRecipe;
val hammer = <immersiveengineering:tool>.withTag({multiblockInterdiction: ["IE:excavator"]});

val og_hammer_recipe = recipes.getRecipesFor(<immersiveengineering:tool>)[0];

recipes.removeShaped(og_hammer_recipe.output, og_hammer_recipe.ingredients2D);
recipes.addShaped(hammer, og_hammer_recipe.ingredients2D);
