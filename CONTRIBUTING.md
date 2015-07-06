# Contribution
---
 1. Make your feature addition or bug fix in a feature branch. (Include a description of your changes)
 2. Push your feature branch to GitHub.
 3. Send a Pull Request.

# Branch Naming
---
* Your feature branch name should show what feature it handles. If it was started from a Redmine issue, begin the branch name with an issue number.

# Ruby Style Guides
---
Following information is based on:

* [Ruby Style Guide by bbatsov](https://github.com/bbatsov/ruby-style-guide)

* [Rails Style Guide by bbatsov](https://github.com/bbatsov/rails-style-guide)

Please refer to these documents, if something is unclear from the text below.


## Source Code Layout
---
* Use UTF-8 as the source file encoding.
* Use two spaces per indentation level (aka soft tabs). No hard tabs.
* Use Unix-style line endings. (BSD/Solaris/Linux/OS X users are covered by default, Windows users have to be extra careful.)
* Don't use ; to separate statements and expressions. As a corollary - use one expression per line.
* Prefer a single-line format for class definitions with no body. 
* Avoid single-line methods. Although they are somewhat popular in the wild, there are a few peculiarities about their definition syntax that make their use undesirable. At any rate - there should be no more than one expression in a single-line method. One exception to the rule are empty-body methods.
* Use spaces around operators, after commas, colons and semicolons, around { and before }. Whitespace might be (mostly) irrelevant to the Ruby interpreter, but its proper use is the key to writing easily readable code.
* The only exception, regarding operators, is the exponent operator.
* No spaces after (, [ or before ], ). 
* No space after !. [link
* No space inside range literals. 
* Indent when as deep as case. I know that many would disagree with this one, but it's the style established in both "The Ruby Programming Language" and "Programming Ruby". 
* When assigning the result of a conditional expression to a variable, preserve the usual alignment of its branches. 
* Use empty lines between method definitions and also to break up a method into logical paragraphs internally. 
* Avoid comma after the last parameter in a method call, especially when the parameters are not on separate lines. 
* Use spaces around the = operator when assigning default values to method parameters. 
* Avoid line continuation \ where not required. In practice, avoid using line continuations for anything but string concatenation. 
* Adopt a consistent multi-line method chaining style. There are two popular styles in the Ruby community, both of which are considered good - leading . (Option A) and trailing . (Option B).
* Align the parameters of a method call if they span more than one line. When aligning parameters is not appropriate due to line-length constraints, single indent for the lines after the first is also acceptable. 
* Align the elements of array literals spanning multiple lines. 
* Add underscores to large numeric literals to improve their readability. 
* Use RDoc and its conventions for API documentation. Don't put an empty line between the comment block and the def. 
* Limit lines to 80 characters. 
* Avoid trailing whitespace. 
* End each file with a newline. 
* Don't use block comments. They cannot be preceded by whitespace and are not as easy to spot as regular comments. 

## Syntax
* Use :: only to reference constants(this includes classes and modules) and constructors (like Array() or Nokogiri::HTML()). Do not use :: for regular method invocation. 
* Use def with parentheses when there are parameters. Omit the parentheses when the method doesn't accept any parameters. 
* Avoid the use of parallel assignment for defining variables. Parallel assignment is allowed when it is the return of a method call, used with the splat operator, or when used to swap variable assignment. Parallel assignment is less readable than separate assignment. It is also slightly slower than separate assignment. 
* Do not use for, unless you know exactly why. Most of the time iterators should be used instead. for is implemented in terms of each (so you're adding a level of indirection), but with a twist - for doesn't introduce a new scope (unlike each) and variables defined in its block will be visible outside it. 
* Do not use then for multi-line if/unless. 
* Always put the condition on the same line as the if/unless in a multi-line conditional. 
* Favor the ternary operator(?:) over if/then/else/end constructs. It's more common and obviously more concise. 
* Use one expression per branch in a ternary operator. This also means that ternary operators must not be nested. Prefer if/else constructs in these cases. 
* Do not use if x; .... Use the ternary operator instead. 
* Leverage the fact that if and case are expressions which return a result. 
* Use when x then ... for one-line cases. The alternative syntax when x: ... has been removed as of Ruby 1.9. 
* Do not use when x; .... See the previous rule. 
* Use ! instead of not. 
* Avoid the use of !!. 
* The and and or keywords are banned. It's just not worth it. Always use && and || instead.
* Avoid multi-line ?: (the ternary operator); use if/unless instead. 
* Favor modifier if/unless usage when you have a single-line body. Another good alternative is the usage of control flow &&/||. 
* Avoid modifier if/unless usage at the end of a non-trivial multi-line block. 
* Favor unless over if for negative conditions (or control flow ||). 
* Do not use unless with else. Rewrite these with the positive case first. 
* Don't use parentheses around the condition of an if/unless/while/until. 
* Do not use while/until condition do for multi-line while/until. 
* Favor modifier while/until usage when you have a single-line body. 
* Favor until over while for negative conditions. 
* Use Kernel#loop instead of while/until when you need an infinite loop. 
* Use Kernel#loop with break rather than begin/end/until or begin/end/while for post-loop tests. 
* Omit parentheses around parameters for methods that are part of an internal DSL (e.g. Rake, Rails, RSpec), methods that have "keyword" status in Ruby (e.g. attr_reader, puts) and attribute access methods. Use parentheses around the arguments of all other method invocations. 
* Omit the outer braces around an implicit options hash. 
* Omit both the outer braces and parentheses for methods that are part of an internal DSL. 
* Omit parentheses for method calls with no arguments. 
* Use the proc invocation shorthand when the invoked method is the only operation of a block.
* Prefer {...} over do...end for single-line blocks. Avoid using {...} for multi-line blocks (multiline chaining is always ugly). Always use do...end for "control flow" and "method definitions" (e.g. in Rakefiles and certain DSLs). Avoid do...end when chaining. 
* Consider using explicit block argument to avoid writing block literal that just passes its arguments to another block. Beware of the performance impact, though, as the block gets converted to a Proc. 
* Avoid return where not required for flow of control. 
* Avoid self where not required. (It is only required when calling a self write accessor.) 
* As a corollary, avoid shadowing methods with local variables unless they are both equivalent.
* Don't use the return value of = (an assignment) in conditional expressions unless the assignment is wrapped in parentheses. This is a fairly popular idiom among Rubyists that's sometimes referred to as safe assignment in condition. 
* Use shorthand self assignment operators whenever applicable. 
* Use ||= to initialize variables only if they're not already initialized. 
* Don't use ||= to initialize boolean variables. (Consider what would happen if the current value happened to be false.) 
* Use &&= to preprocess variables that may or may not exist. Using &&= will change the value only if it exists, removing the need to check its existence with if. 
* Avoid explicit use of the case equality operator ===. As its name implies it is meant to be used implicitly by case expressions and outside of them it yields some pretty confusing code. 
* Do not use eql? when using == will do. The stricter comparison semantics provided by eql?are rarely needed in practice. 
* Avoid using Perl-style special variables (like $:, $;, etc. ). They are quite cryptic and their use in anything but one-liner scripts is discouraged. Use the human-friendly aliases provided by the English library. 
* Do not put a space between a method name and the opening parenthesis. 
* If the first argument to a method begins with an open parenthesis, always use parentheses in the method invocation. For example, write f((3 + 2) + 1). 
* Always run the Ruby interpreter with the -w option so it will warn you if you forget either of the rules above! 
* Do not use nested method definitions, use lambda instead. Nested method definitions actually produce methods in the same scope (e.g. class) as the outer method. Furthermore, the "nested method" will be redefined every time the method containing its definition is invoked. 
* Use the new lambda literal syntax for single line body blocks. Use the lambda method for multi-line blocks. 
* Omit the parameter parentheses when defining a stabby lambda with no parameters. 
* Prefer proc over Proc.new. 
* Prefer proc.call() over proc[] or proc.() for both lambdas and procs. 
* Prefix with _ unused block parameters and local variables. It's also acceptable to use just _(although it's a bit less descriptive). This convention is recognized by the Ruby interpreter and tools like RuboCop and will suppress their unused variable warnings. 
* Use $stdout/$stderr/$stdin instead of STDOUT/STDERR/STDIN. STDOUT/STDERR/STDIN are constants, and while you can actually reassign (possibly to redirect some stream) constants in Ruby, you'll get an interpreter warning if you do so. 
* Use warn instead of $stderr.puts. Apart from being more concise and clear, warn allows you to suppress warnings if you need to (by setting the warn level to 0 via -W0). 
* Favor the use of sprintf and its alias format over the fairly cryptic String#% method.
* Favor the use of Array#join over the fairly cryptic Array#* with  a string argument.
* Use [*var] or Array() instead of explicit Array check, when dealing with a variable you want to treat as an Array, but you're not certain it's an array. 
* Use ranges or Comparable#between? instead of complex comparison logic when possible. 
* Favor the use of predicate methods to explicit comparisons with ==. Numeric comparisons are OK. 
* Don't do explicit non-nil checks unless you're dealing with boolean values. 
* Avoid the use of BEGIN blocks. 
* Do not use END blocks. Use Kernel#at_exit instead. 
* Avoid the use of flip-flops. 
* Avoid use of nested conditionals for flow of control. 
* Prefer a guard clause when you can assert invalid data. A guard clause is a conditional statement at the top of a function that bails out as soon as it can.
* Prefer next in loops instead of conditional blocks.
* Prefer map over collect, find over detect, select over find_all, reduce over injectand size over length. This is not a hard requirement; if the use of the alias enhances readability, it's ok to use it. The rhyming methods are inherited from Smalltalk and are not common in other programming languages. The reason the use of select is encouraged overfind_all is that it goes together nicely with reject and its name is pretty self-explanatory. 
* Don't use count as a substitute for size. For Enumerable objects other than Array it will iterate the entire collection in order to determine its size. 
* Use flat_map instead of map + flatten. This does not apply for arrays with a depth greater than 2, i.e. if users.first.songs == ['a', ['b','c']], then use map + flatten rather than flat_map.  flat_map flattens the array by 1, whereas flatten flattens it all the way. 
* Prefer reverse_each to reverse.each because some classes that include Enumerable will provide an efficient implementation. Even in the worst case where a class does not provide a specialized implementation, the general implementation inherited from Enumerable will be at least as efficient as using reverse.each. 

## Naming
---
* Name identifiers in English. 
* Use snake_case for symbols, methods and variables. 
* Use CamelCase for classes and modules. (Keep acronyms like HTTP, RFC, XML uppercase.) 
* Use snake_case for naming files, e.g. hello_world.rb. 
* Use snake_case for naming directories, e.g. lib/hello_world/hello_world.rb. 
* Aim to have just a single class/module per source file. Name the file name as the class/module, but replacing CamelCase with snake_case. 
* Use SCREAMING_SNAKE_CASE for other constants. 
* The names of predicate methods (methods that return a boolean value) should end in a question mark. (i.e. Array#empty?). Methods that don't return a boolean, shouldn't end in a question mark.
* The names of potentially dangerous methods (i.e. methods that modify self or the arguments, exit! (doesn't run the finalizers like exit does), etc.) should end with an exclamation mark if there exists a safe version of that dangerous method. 
* Define the non-bang (safe) method in terms of the bang (dangerous) one if possible. 
* When using reduce with short blocks, name the arguments |a, e| (accumulator, element). 
* When defining binary operators, name the parameter other(<< and [] are exceptions to the rule, since their semantics are different). 

## Comments
---
* Write self-documenting code and ignore the rest of this section. Seriously! 
* Write comments in English. 
* Use one space between the leading # character of the comment and the text of the comment.
* Comments longer than a word are capitalized and use punctuation. Use one space after periods.
* Avoid superfluous comments. 
* Keep existing comments up-to-date. An outdated comment is worse than no comment at all.
* Avoid writing comments to explain bad code. Refactor the code to make it self-explanatory. (Do or do not - there is no try. --Yoda) 

## Comment Annotations
---

* Annotations should usually be written on the line immediately above the relevant code. 
* The annotation keyword is followed by a colon and a space, then a note describing the problem.
* If multiple lines are required to describe the problem, subsequent lines should be indented three spaces after the # (one general plus two for indentation purpose). 
* In cases where the problem is so obvious that any documentation would be redundant, annotations may be left at the end of the offending line with no note. This usage should be the exception and not the rule. 
* Use TODO to note missing features or functionality that should be added at a later date. 
* Use FIXME to note broken code that needs to be fixed. 
* Use OPTIMIZE to note slow or inefficient code that may cause performance problems. 
* Use HACK to note code smells where questionable coding practices were used and should be refactored away. 
* Use REVIEW to note anything that should be looked at to confirm it is working as intended. For example: REVIEW: Are we sure this is how the client does X currently? 
* Use other custom annotation keywords if it feels appropriate, but be sure to document them in your project's README or similar. 

## Classes & Modules
---
* Use a consistent structure in your class definitions. 
* Don't nest multi line classes within classes. Try to have such nested classes each in their own file in a folder named like the containing class. 
* Prefer modules to classes with only class methods. Classes should be used only when it makes sense to create instances out of them. 
* Favor the use of module_function over extend self when you want to turn a module's instance methods into class methods. 
* When designing class hierarchies make sure that they conform to the Liskov Substitution Principle. 
* Try to make your classes as SOLID as possible. 
* Always supply a proper to_s method for classes that represent domain objects. 
* Use the attr family of functions to define trivial accessors or mutators. 
* Avoid the use of attr. Use attr_reader and attr_accessor instead. 
* Consider using Struct.new, which defines the trivial accessors, constructor and comparison operators for you. 
* Don't extend an instance initialized by Struct.new. Extending it introduces a superfluous class level and may also introduce weird errors if the file is required multiple times. 
* Consider adding factory methods to provide additional sensible ways to create instances of a particular class. 
* Prefer duck-typing over inheritance. 
* Avoid the usage of class (@@) variables due to their "nasty" behavior in inheritance. 
* Assign proper visibility levels to methods (private, protected) in accordance with their intended usage. Don't go off leaving everything public (which is the default). After all we're coding in Ruby now, not in Python. 
* Indent the public, protected, and private methods as much as the method definitions they apply to. Leave one blank line above the visibility modifier and one blank line below in order to emphasize that it applies to all methods below it. 
* Use def self.method to define class methods. This makes the code easier to refactor since the class name is not repeated. 
* Prefer alias when aliasing methods in lexical class scope as the resolution of self in this context is also lexical, and it communicates clearly to the user that the indirection of your alias will not be altered at runtime or by any subclass unless made explicit. 
* Since alias, like def, is a keyword, prefer bareword arguments over symbols or strings. In other words, do alias foo bar, not alias :foo :bar.
* Also be aware of how Ruby handles aliases and inheritance: an alias references the method that was resolved at the time the alias was defined; it is not dispatched dynamically.
* Always use alias_method when aliasing methods of modules, classes, or singleton classes at runtime, as the lexical scope of alias leads to unpredictability in these cases. 

## Exceptions
---
* Signal exceptions using the fail method. Use raise only when catching an exception and re-raising it (because here you're not failing, but explicitly and purposefully raising an exception). 
* Don't specify RuntimeError explicitly in the two argument version of fail/raise. 
* Prefer supplying an exception class and a message as two separate arguments to fail/raise, instead of an exception instance. 
* Do not return from an ensure block. If you explicitly return from a method inside an ensureblock, the return will take precedence over any exception being raised, and the method will return as if no exception had been raised at all. In effect, the exception will be silently thrown away. 
* Use implicit begin blocks where possible. 
* Mitigate the proliferation of begin blocks by using contingency methods (a term coined by Avdi Grimm). 
* Don't suppress exceptions. 
* Avoid using rescue in its modifier form. 
* Don't use exceptions for flow of control. 
* Avoid rescuing the Exception class. This will trap signals and calls to exit, requiring you to kill -9 the process. 
* Put more specific exceptions higher up the rescue chain, otherwise they'll never be rescued from. 
* Release external resources obtained by your program in an ensure block. 
* Use versions of resource obtaining methods that do automatic resource cleanup when possible.
* Favor the use of exceptions for the standard library over introducing new exception classes. 

## Collections
---
* Prefer literal array and hash creation notation (unless you need to pass parameters to their constructors, that is). 
* Prefer %w to the literal array syntax when you need an array of words (non-empty strings without spaces and special characters in them). Apply this rule only to arrays with two or more elements.
* Prefer %i to the literal array syntax when you need an array of symbols (and you don't need to maintain Ruby 1.9 compatibility). Apply this rule only to arrays with two or more elements. 
* Avoid comma after the last item of an Array or Hash literal, especially when the items are not on separate lines. 
* Avoid the creation of huge gaps in arrays. 
* When accessing the first or last element from an array, prefer first or last over [0] or [-1]. 
* Use Set instead of Array when dealing with unique elements. Set implements a collection of unordered values with no duplicates. This is a hybrid of Array's intuitive inter-operation facilities and Hash's fast lookup. 
* Prefer symbols instead of strings as hash keys. 
* Avoid the use of mutable objects as hash keys. 
* Use the Ruby 1.9 hash literal syntax when your hash keys are symbols. 
* Don't mix the Ruby 1.9 hash syntax with hash rockets in the same hash literal. When you've got keys that are not symbols stick to the hash rockets syntax. 
* Use Hash#key? instead of Hash#has_key? and Hash#value? instead of Hash#has_value?. As noted here by Matz, the longer forms are considered deprecated. 
* Use Hash#fetch when dealing with hash keys that should be present. 
* Introduce default values for hash keys via Hash#fetch as opposed to using custom logic. 
* Prefer the use of the block instead of the default value in Hash#fetch if the code that has to be evaluated may have side effects or be expensive. 
* Use Hash#values_at when you need to retrieve several values consecutively from a hash. 
* Rely on the fact that as of Ruby 1.9 hashes are ordered. 
* Do not modify a collection while traversing it. 
* When accessing elements of a collection, avoid direct access via [n] by using an alternate form of the reader method if it is supplied. This guards you from calling [] on nil. 
* When providing an accessor for a collection, provide an alternate form to save users from checking for nil before accessing an element in the collection. 

## Strings
---
* Prefer string interpolation and string formatting instead of string concatenation: 
* With interpolated expressions, there should be no padded-spacing inside the braces. 
* Adopt a consistent string literal quoting style. There are two popular styles in the Ruby community, both of which are considered good - single quotes by default (Option A) and double quotes by default (Option B). 
* The string literals in this guide are aligned with the first style.
* Don't use the character literal syntax ?x. Since Ruby 1.9 it's basically redundant - ?x would interpreted as 'x' (a string with a single character in it). 
* Don't leave out {} around instance and global variables being interpolated into a string. 
* Don't use Object#to_s on interpolated objects. It's invoked on them automatically. 
* Avoid using String#+ when you need to construct large data chunks. Instead, use String#<<. Concatenation mutates the string instance in-place and is always faster than String#+, which creates a bunch of new string objects. 
* Don't use String#gsub in scenarios in which you can use a faster more specialized alternative.
* When using heredocs for multi-line strings keep in mind the fact that they preserve leading whitespace. It's a good practice to employ some margin based on which to trim the excessive whitespace. 

## Regular Expressions
---
* Don't use regular expressions if you just need plain text search in string: string['text']
* For simple constructions you can use regexp directly through string index. 
* Use non-capturing groups when you don't use captured result of parentheses. 
* Don't use the cryptic Perl-legacy variables denoting last regexp group matches ($1, $2, etc). Use Regexp.last_match(n) instead. 
* Avoid using numbered groups as it can be hard to track what they contain. Named groups can be used instead. 
* Character classes have only a few special characters you should care about: ^, -, \, ], so don't escape . or brackets in []. 
* Be careful with ^ and $ as they match start/end of line, not string endings. If you want to match the whole string use: \A and \z (not to be confused with \Z which is the equivalent of /\n?\z/). 
* Use x modifier for complex regexps. This makes them more readable and you can add some useful comments. Just be careful as spaces are ignored. 
* For complex replacements sub/gsub can be used with block or hash. 

## Percent Literals
---
* Use %()(it's a shorthand for %Q) for single-line strings which require both interpolation and embedded double-quotes. For multi-line strings, prefer heredocs. 
* Avoid %q unless you have a string with both ' and " in it. Regular string literals are more readable and should be preferred unless a lot of characters would have to be escaped in them.
* Use %r only for regular expressions matching at least one '/' character. 
* Avoid the use of %x unless you're going to invoke a command with backquotes in it(which is rather unlikely). 
* Avoid the use of %s. It seems that the community has decided :"some string" is the preferred way to create a symbol with spaces in it. 
* Prefer () as delimiters for all % literals, except %r. Since parentheses often appear inside regular expressions in many scenarios a less common character like { might be a better choice for a delimiter, depending on the regexp's content. 

## Metaprogramming
---
* Avoid needless metaprogramming. 
* Do not mess around in core classes when writing libraries. (Do not monkey-patch them.) 
* Prefer public_send over send so as not to circumvent private/protected visibility. 

## Misc
---
* Write ruby -w safe code. 
* Avoid hashes as optional parameters. Does the method do too much? (Object initializers are exceptions for this rule). 
* Avoid methods longer than 10 LOC (lines of code). Ideally, most methods will be shorter than 5 LOC. Empty lines do not contribute to the relevant LOC. 
* Avoid parameter lists longer than three or four parameters. 
* If you really need "global" methods, add them to Kernel and make them private. 
* Use module instance variables instead of global variables. 
* Use OptionParser for parsing complex command line options and ruby -s for trivial command line options. 
* Prefer Time.now over Time.new when retrieving the current system time. 
* Code in a functional way, avoiding mutation when that makes sense. 
* Do not mutate parameters unless that is the purpose of the method. 
* Avoid more than three levels of block nesting. 
* Be consistent. In an ideal world, be consistent with these guidelines. 
* Use common sense.

# The Rails Style Guide
---
## Configuration
---
* Put custom initialization code in config/initializers. The code in initializers executes on application startup. 
* Keep initialization code for each gem in a separate file with the same name as the gem, for example carrierwave.rb, active_admin.rb, etc. 
* Adjust accordingly the settings for development, test and production environment (in the corresponding files under config/environments/) 
* Keep configuration that's applicable to all environments in the config/application.rb file. 
* Create an additional staging environment that closely resembles the production one. 
* Keep any additional configuration in YAML files under the config/ directory. 
* Since Rails 4.2 YAML configuration files can be easily loaded with the new config_for method.

## Routing
---
* When you need to add more actions to a RESTful resource (do you really need them at all?) use member and collection routes. 
* If you need to define multiple member/collection routes use the alternative block syntax. 
* Use nested routes to express better the relationship between ActiveRecord models. 
* Use namespaced routes to group related actions. 
* Never use the legacy wild controller route. This route will make all actions in every controller accessible via GET requests. 
* Don't use match to define any routes unless there is need to map multiple request types among [:get, :post, :patch, :put, :delete] to a single action using :via option. 

## Controllers
---

* Keep the controllers skinny - they should only retrieve data for the view layer and shouldn't contain any business logic (all the business logic should naturally reside in the model). 
* Each controller action should (ideally) invoke only one method other than an initial find or new.
* Share no more than two instance variables between a controller and a view. 

## Models
---
* Introduce non-ActiveRecord model classes freely. 
* Name the models with meaningful (but short) names without abbreviations. 

* If you need model objects that support ActiveRecord behavior (like validation) without the ActiveRecord database functionality use the ActiveAttr gem. 

## ActiveRecord
---
* Avoid altering ActiveRecord defaults (table names, primary key, etc) unless you have a very good reason (like a database that's not under your control). 
* Group macro-style methods (has_many, validates, etc) in the beginning of the class definition.
* Prefer has_many :through to has_and_belongs_to_many. Using has_many :through allows additional attributes and validations on the join model. 
* Prefer self[:attribute] over read_attribute(:attribute). 
* Prefer self[:attribute] = value over write_attribute(:attribute, value). 
* Always use the new "sexy" validations. 
* When a custom validation is used more than once or the validation is some regular expression mapping, create a custom validator file. 
 Keep custom validators under app/validators. 
* Consider extracting custom validators to a shared gem if you're maintaining several related apps or the validators are generic enough. 
* Use named scopes freely. 
* When a named scope defined with a lambda and parameters becomes too complicated, it is preferable to make a class method instead which serves the same purpose of the named scope and returns an ActiveRecord::Relation object. Arguably you can define even simpler scopes like this.
* Beware of the behavior of the update_attribute method. It doesn't run the model validations (unlike update_attributes) and could easily corrupt the model state. 
* Use user-friendly URLs. Show some descriptive attribute of the model in the URL rather than its id. There is more than one way to achieve this: 
* Override the to_param method of the model. This method is used by Rails for constructing a URL to the object. The default implementation returns the id of the record as a String. It could be overridden to include another human-readable attribute. In order to convert this to a URL-friendly value, parameterize should be called on the string. The id of the object needs to be at the beginning so that it can be found by the find method of ActiveRecord.
* Use the friendly_id gem. It allows creation of human-readable URLs by using some descriptive attribute of the model instead of its id. 
* Use find_each to iterate over a collection of AR objects. Looping through a collection of records from the database (using the all method, for example) is very inefficient since it will try to instantiate all the objects at once. In that case, batch processing methods allow you to work with the records in batches, thereby greatly reducing memory consumption. 
* Since Rails creates callbacks for dependent associations, always call before_destroy callbacks that perform validation with prepend: true. 

## ActiveRecord Queries
---
* Avoid string interpolation in queries, as it will make your code susceptible to SQL injection attacks. 
* Consider using named placeholders instead of positional placeholders when you have more than 1 placeholder in your query. 
* Favor the use of find over where when you need to retrieve a single record by id. 
* Favor the use of find_by over where when you need to retrieve a single record by some attributes. 
* Use find_each when you need to process a lot of records. 
* Favor the use of where.not over SQL. 

## Migrations
---
* Keep the schema.rb (or structure.sql) under version control. 
* Use rake db:schema:load instead of rake db:migrate to initialize an empty database. 
* Enforce default values in the migrations themselves instead of in the application layer. 
* While enforcing table defaults only in Rails is suggested by many Rails developers, it's an extremely brittle approach that leaves your data vulnerable to many application bugs. And you'll have to consider the fact that most non-trivial apps share a database with other applications, so imposing data integrity from the Rails app is impossible.
* Enforce foreign-key constraints. As of Rails 4.2, ActiveRecord supports foreign key constraints natively. 
* When writing constructive migrations (adding tables or columns), use the change method instead of up and down methods. 
* Don't use model classes in migrations. The model classes are constantly evolving and at some point in the future migrations that used to work might stop, because of changes in the models used. 

## Views
---
* Never call the model layer directly from a view. 
* Never make complex formatting in the views, export the formatting to a method in the view helper or the model. 
* Mitigate code duplication by using partial templates and layouts. 

# Internationalization
---
* No strings or other locale specific settings should be used in the views, models and controllers. These texts should be moved to the locale files in the config/locales directory. 
* When the labels of an ActiveRecord model need to be translated, use the active record scope.
* Then User.model_name.human will return "Member" and User.human_attribute_name("name") will return "Full name". These translations of the attributes will be used as labels in the views.
* Separate the texts used in the views from translations of ActiveRecord attributes. Place the locale files for the models in a folder models and the texts used in the views in folder views. 
* When organization of the locale files is done with additional directories, these directories must be described in the application.rb file in order to be loaded.
 Place the shared localization options, such as date or currency formats, in files under the root of the locales directory. 
* Use the short form of the I18n methods: I18n.t instead of I18n.translate and I18n.linstead of I18n.localize. 
* Use "lazy" lookup for the texts used in views. 
* Use the dot-separated keys in the controllers and models instead of specifying the :scopeoption. The dot-separated call is easier to read and trace the hierarchy.  More detailed information about the Rails I18n can be found in the Rails Guides 

## Assets
---
* Use the assets pipeline to leverage organization within your application.
* Reserve app/assets for custom stylesheets, javascripts, or images. 
* Use lib/assets for your own libraries that don’t really fit into the scope of the application. 
* Third party code such as jQuery or bootstrap should be placed in vendor/assets. 
* When possible, use gemified versions of assets (e.g. jquery-rails, jquery-ui-rails, bootstrap-sass,zurb-foundation). 

## Mailers
---
* Name the mailers SomethingMailer. Without the Mailer suffix it isn't immediately apparent what's a mailer and which views are related to the mailer. 
* Provide both HTML and plain-text view templates. 
* Enable errors raised on failed mail delivery in your development environment. The errors are disabled by default. 
* Use a local SMTP server like Mailcatcher in the development environment. 
* Provide default settings for the host name. 
* If you need to use a link to your site in an email, always use the _url, not _path methods. The _url methods include the host name and the _path methods don't. 
* Format the from and to addresses properly. Use the following format: 
* Make sure that the e-mail delivery method for your test environment is set to test. 
* The delivery method for development and production should be smtp. 
* When sending html emails all styles should be inline, as some mail clients have problems with external styles. This however makes them harder to maintain and leads to code duplication. There are two similar gems that transform the styles and put them in the corresponding html tags: premailer-rails and roadie. 
* Sending emails while generating page response should be avoided. It causes delays in loading of the page and request can timeout if multiple email are sent. To overcome this emails can be sent in background process with the help of sidekiq gem. 

## Time
---
* Config your timezone accordingly in application.rb. 
* Don't use Time.parse. 
* Don't use Time.now. 

## Bundler
---

* Put gems used only for development or testing in the appropriate group in the Gemfile. 

* Use only established gems in your projects. If you're contemplating on including some little-known gem you should do a careful review of its source code first. 

* OS-specific gems will by default result in a constantly changing Gemfile.lock for projects with multiple developers using different operating systems. Add all OS X specific gems to a darwingroup in the Gemfile, and all Linux specific gems to a linux group: 
* Do not remove the Gemfile.lock from version control. This is not some randomly generated file - it makes sure that all of your team members get the same gem versions when they do a bundle install. 

## Flawed Gems
---
* This is a list of gems that are either problematic or superseded by other gems. You should avoid using them in your projects.
* rmagick - this gem is notorious for its memory consumption. Use minimagick instead.

* autotest - old solution for running tests automatically. Far inferior to guard and watchr.

* rcov - code coverage tool, not compatible with Ruby 1.9. Use SimpleCov instead.

* therubyracer - the use of this gem in production is strongly discouraged as it uses a very large amount of memory. I'd suggest using node.js instead.

* This list is also a work in progress. Please, let me know if you know other popular, but flawed gems.

* Managing processes

* If your projects depends on various external processes use foreman to manage them. 