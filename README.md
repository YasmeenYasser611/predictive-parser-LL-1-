# predictive-parser-LL-1-
We have designed predictive parser LL (1) That will parse any if-else statement or while statement or both according to the following CFG, then draw the parse tree of this statements.
the CFG:
stmts→ stmt  stmts | ε
stmt → assign_stmt | while_stmt|if_else_stmt|{stmts}
assign_stmt → id = exp ;
while_stmt → while ( cond ) { stmts } 
if_else_stmt → if ( cond ) stmt  opt_stmt
opt_stmt → else stmt | ε 
cond → id op exp 
op→> | < | >= | <= | =|……. 
exp → term R 
R → + term R | - term R | ε 
term→ factor R1 
R1 → * factor R1 | / factor R1 | ε 
factor → id | digits | ( exp ) 
digits → digit digits | ε
id → a|……|z|A|……|Z
digit → 0|1|…..|9
