-------------------------------------------------------------------------------
## Code block


### Usage:
	<% code %>
    
        # Content
    
    <~ code %>


### Example:

#### Input string:
	<% code %>
	
	a = 1
	b = 2
	c = a + b
		
	<~ c %> 

-------------------------------------------------------------------------------
## Expression evaluation


### Usage:

	<= expression %>


### Example:

#### Input:
	<% code %>
	
	a = 2 + 2
	
	<~ code %>
	
	
	Value of a is <= a %>.
	
#### Output:
	Value of a is 4.
    
-------------------------------------------------------------------------------
## Conditional statements


### Usage:
    <% if 'conditional_expression' %>
    
        # Content
    
    <% elif 'another_expression' %>
    
        # Content
		
	<% else %>
	
		# Content
		
    <~ if %>


### Example:

#### Input:
	<% code %>
		a = 23
		b = 32
		printA = False
		printB = True
	<~ code %>

	<% if printA %>
		Value of a is <= a %>.
	<% elif printB %>
		Value of b is <= b %>.
	<~ if %>
	
#### Output:
	Value of b is 32.

-------------------------------------------------------------------------------
## For loop


### Usage:
    <% for 'values' in 'container' %>
    
        # Content
    
    <~ for %>


### Example:

#### Input:
	<% for i in range(2) %>
	
		Value of i is <= i %>.
		
		<% if i == 0 %>
			First iteration.
		<% elif i == 1 %>
			Second iteration.
		<~ if %>
		
	<~ for %>
	
#### Output:
	Value of i is 0.
	First iteration.
	
	Value of i is 1.
	Second iteration.

-------------------------------------------------------------------------------
## While loop


### Usage:
	<% while 'condition' %>
	
		# Content
		
	<~ while %>


### Example:

#### Input:
	<% code %>
	a = 3
	<~ code %>
	
	<% while a > 0 %>
	
		Value of a is <= a >
		
		<% code %>
			a -= 1
		<~ code >
	
	<~ while %>

#### Output:
	Value of a is 3
	Value of a is 2
	Value of a is 1

-------------------------------------------------------------------------------
## include tag


### Description:

The "include" tag allows for file inclusion. Generator searches predefined
locations added via "Generator.addSearchPath" for the given file. If file
is not found in any of those locations, custom handlers added via
"Generator.addSearchHandler" are invoked allowing for "memory" file loading.

### Usage:
	<% include file_name.py %>


### Example:

#### example_file.py contents:
    Hello from example_file.py!
    <% code %>
        example_file_var = 42
    <~ code %> 
		
#### Input:
    <% include example_file.py %>
	
    Value of example file var is <= example_file_var %>.

#### Output:
    Hello from example_file.py!
		
    Value of example file var is 42.

-------------------------------------------------------------------------------