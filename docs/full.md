# Dokumentacja Projektowa

---

<details>
  <summary><b>Spis Treści</b></summary>

Spis Treści
=================

* [Streszczenie](#streszczenie)
* [Projekt Wstępny](#projekt-wstępny)
    * [Opis zakładanej funkcjonalności](#opis-zakładanej-funkcjonalności)
        * [System typów](#system-typów)
        * [Zmienne i typy danych](#zmienne-i-typy-danych)
        * [Operacje](#operacje)
        * [Konstrukcje](#konstrukcje)
        * [Struktury](#struktury)
        * [Inne](#inne)
    * [Konstrukcje językowe - przykłady](#konstrukcje-językowe---przykłady)
        * [System typów](#system-typów-1)
        * [Zmienne i typy danych](#zmienne-i-typy-danych-1)
        * [Operacje](#operacje-1)
        * [Konstrukcje](#konstrukcje-1)
        * [Struktury](#struktury-1)
        * [Inne](#inne-1)
    * [Gramatyka](#gramatyka)
        * [Znaki](#znaki)
        * [Symbole terminalne](#symbole-terminalne)
        * [Symbole nieterminale](#symbole-nieterminalne)
    * [Obsługa błędów](#obsługa-błędów)
        * [Lekser](#lekser)
        * [Parser](#parser)
        * [Interpreter i analizatory semantyczne](#interpreter-i-analizatory-semantyczne)
        * [Mechanizm panikowania](#mechanizm-panikowania)
    * [Analiza wymagań funkcjonalnych](#analiza-wymagań-funkcjonalnych)
* [Rozwiązanie](#rozwiązanie)
    * [Skrócony opis implementacji](#skrócony-opis-implementacji)
        * [Common](#common)
        * [Lexer](#lexer)
        * [Parser](#parser-1)
        * [Tools](#tools)
        * [Utils](#utils)
    * [Uzasadnienie decyzji implementacyjnych](#uzasadnienie-decyzji-implementacyjnych)
    * [Problemy i trudności](#problemy-i-trudności)
        * [Lekser](#lekser-1)
        * [Parser](#parser-2)
        * [Interpreter](#interpreter)
    * [Użycie](#użycie)

</details>

# Streszczenie

---

Celem projektu jest stworzenie nowego języka programowania, który będzie
statycznie i słabo typowany. Język ten będzie oferował niemutowalne zmienne
jako domyślną opcję oraz będzie zapewniał obsługę podstawowych
typów danych, takich jak liczby całkowite (`i32`), zmiennoprzecinkowe (`f32`),
wartości logiczne (`bool`) i ciągi znaków (`str`).

Kluczowe funkcjonalności języka obejmują:

- **System typów**: Zapewnia statyczne sprawdzanie typów i inferencję typów
  deklaracji zmiennych.
- **Operacje matematyczne i logiczne**: Obsługa standardowych operatorów
  arytmetycznych, logicznych oraz operacji na ciągach znaków.
- **Konstrukcje językowe**: Umożliwia tworzenie struktur kontrolnych, takich
  jak pętle i instrukcje warunkowe.

Projekt zakłada uwzględnienie analizę wymagań funkcjonalnych oraz testowanie
kodu od początku implementacji.

# Projekt

---

## Opis zakładanej funkcjonalności

### System typów

1. Język jest statycznie typowany
2. Język jest słabo typowany
3. Język wspiera inferencję typów

### Zmienne i typy danych

1. Zmienne domyślnie są niemutowalne.
2. Język wspiera wbudowane typy danych:
    - Całkowitoliczbowe: `i32`
    - Zmiennoprzecinkowe: `f32`
    - Boolowskie: `bool`
    - Ciągi znaków: `str` (zawierający dowolne znaki, włącznie z wyróżnikiem,
      nową linią oraz tabulacją)
3. Zmienne mogą występować w kontekście globalnym oraz lokalnym.
4. Zmienne w kontekście lokalnym są usuwane po wyjściu z kontekstu.
5. Zmienne są przekazywane do najbliższego kontekstu.

### Operacje

1. Stosowanie operatorów zgodne jest z konwencją stosowaną w matematyce:
    - Nawiasowanie przed mnożeniem/dzieleniem.
    - Mnożenie/dzielenie przed dodawaniem/odejmowaniem.
    - Znak minusa przed dodawaniem/odejmowaniem.
2. Interpreter ma wbudowane operacje:
    - Dla typów liczbowych: `+`, `-`, `/`, `*`, `<`, `>`
    - Dla typów boolowskich: `&&`, `||`, `!`
    - Dla typów znakowych: `+` (konkatenacji), `*` (replikacja)
    - Dla wszystkich: `==`, `!=` (o ile są castowalne do `bool`)
3. Operacje na typach powodują wywołanie stosownej funkcji realizującej daną
   operację.
    - W przypadku braku znalezienia odpowiedniej funkcji zostaje wykorzystany
      mechanizm panikowania.

### Konstrukcje

1. Język obsługuje konstrukcję warunkową `if-else`.
2. Język obsługuje pętlę `while`.
3. Język zapewnia mechanizm panikowania `panic`.
    - Użycie mechanizmu panikowania kończy interpretację programu oraz
      wyświetla komunikat o błędzie oraz linii kodu, z którego on pochodzi.
4. Język pozwala na definicję funkcji.
    - Argumenty przekazywane są przez wartość.
    - Możliwe jest wywoływanie rekurencyjne funkcji - maksymalna głębokość
      regulowana jest przez flagę interpretera.
    - Funkcje zwracają wartość zgodną z adnotacją zwracanego typu - w przypadku
      jej braku funkcje nic nie zwracaja tzw. `void`
    - Każda ścieżka wykonywania w funkcji musi zwrócić wartość.
    - Wartości przy wywołaniu funkcji nie są automatycznie rzutowane do
      odpowiedniego typu.
5. Język obsługuję konstrukcję `match`:
    - Konstrukcja pozwala na sprawdzenie - dopasowanie typu wyrażenia do
      zdefiniowanych typów.
    - Dopasowanie typu powoduje wykonanie bloku przypisanego do tego typu.
    - Możliwe jest zdefiniowanie domyślnego przypadku poprzez zapis typu
      jako `_`
    - Wartość będąca w kontekście wykonywanego bloku konstrukcji match jest
      referencją.

### Struktury

1. Język obsługuje struktury:
    - Struktura może posiadać pola o dowolnym typie.
    - Język pozwala na odczyt/zapis pól w strukturach.
    - Wszystkie pola w strukturach są publiczne.
    - Pola w obrębie struktury muszą być unikalne.
2. Język obsługuje rekordy wariantowe.
    - Możliwe jest sprawdzenie czy rekord jest danym wariantem / danego typu.
    - Możliwe jest rzutowanie tylko do odpowiedniego wariantu - próba
      rzutowania do innego wariantu zakończy się spanikowaniem programu.
3. Struktury traktowane są jako typy zdefiniowane przez użytkownika:
    - Dozwolone jest wykorzystanie struktur jako typów argumentów funkcji.

### Inne

1. Język wspiera komentarze jednolinijkowe - koniec komentarza wyznaczony jest
   przez znak nowej linii lub znak końca pliku.
2. Rzutowanie typów dokonywane przez interpreter dokonywane jest automatycznie
   dla predefiniowanych zestawów typów.
3. Interpreter posiada wbudowane funkcje do wyświetlania oraz pobierania
   danych.
4. Możliwe jest rzutowanie ręczne typów.

## Konstrukcje językowe - przykłady

### System typów

```rust
// 1. Statyczne typowanie
let mut x: i32 = 10;
x = "var"; // panic!; mismatched type

// 2. Słabe typowanie
let x: i32 = 10;
let y: f32 = x + 2.0; // y = 12.0

// 3. Inferencja
let x = 10.3; // x: f32
```

### Zmienne i typy danych

```rust
// 1. Niemutowalne zmienne
let x: i32 = 3;
let mut y: i32 = 4;
y = y + 1; // y = 5;
x = x + 1; // panic!: cannot assign twice to immutable variable 'x'

// 2. Typy danych
let x: i32 = 10;
let z: f32 = 3.14;
let d: bool = true;
let e: str = "Print\n\"line\"" // escaping \n \"

// 3. & 5. Kontekst oraz przesłanianie 
let y: i32 = 10;

fn x() {
    let y: i32 = 20;
    let x: i32 = y + 0; // x = 20;
}

// 4. Usuwanie zmiennych po wyjściu z kontekstu
fn x(y: i32) {
    if (y > 10) {
        let z: i32 = 20;
    }

    let d: i32 = z + 0; // panic!: undefined variable 'z';
}
```

### Operacje

```rust
// 1. Priorytety
let x: i32 = (1 * 3) + 4; // x = (1 * 3) + 4 => x = 3 + 4 => x = 7;

// 2. Wbudowane operacje
let y: f32 = 3.14 + 10; // y = 13.14;
let z: bool = y > 10 && y < 20; // z = true;
let d: str = "Hello" + "World"; // d = "HelloWorld";

// 3. Wywołanie funkcji wbudowanej
let x: i32 = (1 * 3) + 4; // x = __add(__mul(1, 3), 4);
let y: i32 = "Example" / "E"; // panic!: undefined operation "/" for "str" and "str"
```

### Konstrukcje

1. Konstrukcja warunkowa `if-else`

```rust
// <> - miejsce do wstawienia 
// [] - opcjonalne
if (<condition>) {
    <if-block>
} [else {
    <else-block>
}]
```

- W przypadku spełnienia warunku konstrukcji warunkowej `<condition>` zostanie
  wykonany blok `<if-block>`.
- W przeciwnym wypadku zostanie wykonany blok `<else-block>`.

```rust
let x: i32 = 6;

if (x > 5) {
    println("gt");
} else {
    println("le");
}
```

2. Pętla `while`

```rust
// <> - miejsce do wstawienia 
// [] - opcjonalne
while (<condition>) {
    <while-block>
}
```

- W przypadku spełnienia warunku `<condition>` zostanie wykonany
  blok `<while-block>`.
- Po każdym wykonaniu bloku `<while-block>` ponownie zostanie wykonany krok
  poprzedni.
- Wyjście z pętli (przekazanie sterowania dalej) może nastąpić poprzez
  niespełnienie warunku `<condition>` lub przez wyjście z funkcji `return`

```rust 
let mut x: i32 = 0;
while (x < 10) {
    x = x + 1;
    println("x = " + x);
}
```

3. Mechanizm panikowania

```rust
fn div(x: i32, y: i32) -> i32 {
    if (y == 0) {
        panic("Cannot divide by zero");
    }

    return x / y;
}

div(3, 0); // panic!: Cannot divide by zero. Panicked at line: 3, main.fhll
```

4. Definiowanie funkcji

```rust
// <> - miejsce do wstawienia 
// [] - wielokrotność / opcjonalność
fn <name> ([, <arg>]) -> [type] {
    <fn-block>
}
```

- Funkcja definiowana jest poprzez nazwę `<name>` oraz zbiór typów
  argumentów `[<arg>]`.
- Argumenty przekazywane są przez wartość.

```rust
fn square(mut x: i32) -> i32 {
    x = x * x;
    return x;
}
```

```rust
let mut x: i32 = 0;
square(x);
let z: i32 = x; // z = 0;
```

5. Konstrukcja `match`

- Konstrukcja dokonuje sprawdzenia typu wyrażenia i wykonania bloku kodu, który
  jest przypisany do danego typu
- W przypadku braku dopasowania wykonywany jest domyślny blok kodu, o ile
  został zdefiniowany
- w przypadku dopasowania do wielu bloków wykonywany jest jedynie pierwszy (
  względem zdefiniowana blok kodu)

```rust
// <> - miejsce do wstawienia 
// [] - wielokrotność / opcjonalność
match (<expression>) {
    <type> <name> => {
        // code for another type
    };
    <type> <name> => {
        // code for another type
    };
    _ <name> => {
        // code for default case
    };
}
```

```rust
enum Item {
    Fruit {
        nutrition: u32;
    };

    Tool {
        name: str;  
    };
}

let item: Item = Fruit { nutrition = 2; };
match (item) {
    Item::Fruit fruit => {
        // item now has type Item::Fruit
        writeln("It is a fruit with nutrition: " + fruit.nutrition);
    };
    Item::Tool tool => {
        // item now has type Item::Tool
        writeln("It is a tool with name: " + tool.name);
    };
    _ x => {
        panic("Expected item");
    };
}
```

### Struktury

1. Struktury

```rust
// <> - miejsce do wstawienia 
// [] - wielokrotność / opcjonalność
struct <name> {
    [<fieldName>: <fieldType>;]
}
```

- Struktura posiada swoją nazwę `<name>` oraz listę publicznych
  pól `[<fieldName>]`.
- Każde pole struktury musi mieć określony typ.
- Pola struktur domyślnie inicjalizowane są wartościami domyślnymi - w
  przypakdu gdy polem jest inna struktura, zostanie ona domyślnie
  zainicjalizowana

```rust
struct Item {
    name: str;
    amount: i32;
}

let item = Item { name: "Axe"; amount: 1; };
println(item.name);
item.amount = 4;
```

```rust
struct Inventory {
    item: Item;
    name: str;
}

let inventory: Inventory; // let inventory = Inventory { name = ""; item = Item { name = ""; amount = 0; }}; 
```

2. Rekordy wariantowe

```rust
enum <name> {
    struct <variant> {
        <variantField>: <variantFieldType>
    };
    enum <variant> {
    
    };
}
```

- Rekordy wariantowe posiadają swoją nazwę `<name>` oraz mogą zawierać dowolną
  liczbę wariantów `<variant>` - będących strukturami lub rekordami
- Każdy wariant posiada listę swoich pól `[<variantField>]` wraz z ich typami
  lub listę wariantów w przypadku rekordu wariantowego

```rust
enum Entity {
    struct Player {
        firstname: str;
    };

    struct Animal {
        name: str;
    };
}

let e: Entity = Entity::Player { firstname = "John"; };
if (e is Entity::Player) {
    let f = e as Entity::Player;
}
```

3. Struktury jako typy zdefiniowane przez użytkownika

```rust
fn calculate_cost(item: Item, cost_per_item: i32) -> i32 {
    return item.amount * cost_per_item;
}
```

### Inne

1. Komentarze

```rust
// comment
```

2. Rzutowanie automatyczne

```rust
let y: f32 = 1; // y = 1.0;
```

3. Wbudowane funkcje i/o

```rust
println("Hello World");
let x: i32 = readi32();
```

4. Rzutowanie typów

```rust
let x = 3 as f32; // x: f32
```

## Gramatyka

### Znaki

```
letter              ::= "a" ... "z" | "A" ... "Z";
letter_or_under     ::= letter | "_";
digit               ::= "0" ... "9";
unicode             ::= // whole unicode;
```

### Symbole terminalne

```
identifier          ::= letter_or_under, { letter_or_under | digit };

builtin_type        ::= "i32" 
                      | "f32"
                      | "bool"
                      | "str";

keyword             ::= "fn"
                      | "struct"
                      | "enum"
                      | "mut"
                      | "let"
                      | "is"
                      | "if"
                      | "while"
                      | "return"
                      | "as"
                      | "match";

integer_literal     ::= "0" 
                       | ("1" ... "9"), { digit };
float_literal       ::= integer_literal, ".", digit, { digit };
string_literal      ::= \" { unicode } \";
literal             ::= integer_literal
                       | float_literal
                       | string_literal;

and_op              ::= "&&";
or_op               ::= "||";
relation_op         ::= "=="
                       | "!="
                       | "<"
                       | ">";
additive_op         ::= "+" 
                       | "-";
multiplicative_op   ::= "*" 
                       | "/";
unary_op            ::= "-"
                       | "!";

assign_op           ::= "=";

left_parentheses    ::= "(";
left_bracket        ::= "{";
right_parentheses   ::= ")";
right_bracket       ::= "}";

type_adnotation     ::= ":";
rtype_adnotation    ::= "->";

field_access        ::= ".";
variant_access      ::= "::";

match_op            ::= "=>";

period              ::= ",";
separator           ::= ";";
```

### Symbole nieterminalne

```
Module              ::= { FunctionDeclaration | StructDeclaration | EnumDeclaration };

FunctionDeclaration ::= "fn", identifier, "(", [ Parameters ], ")", [ "->", Type ], Block;
Parameters          ::= Parameter, { ",", Parameter };
Parameter           ::= [ "mut" ], identifier, ":", Type;

StructDeclaration   ::= "struct", identifier, "{", { FieldDeclaration }, "}";
FieldDeclaration    ::= identifier, ":", Type, ";";

EnumDeclaration     ::= "enum", identifier, "{", { VariantDeclaration }, "}";
VariantDeclaration  ::= EnumDeclaration 
                      | StructDeclaration;

Block               ::= "{", StatementList, "}";

StatementList       ::= { (Statement, ";") | BlockStatement }
Statement           ::- Declaration 
                      | Assignment
                      | FnCall
                      | ReturnStatement;
BlockStatement      ::= Block
                      | IfStatement
                      | WhileStatement
                      | MatchStatement;

Declaration         ::= [ "mut" ], "let", identifier, [ ":", Type ], [ "=", Expression ];
Assignment          ::= Access, "=", Expression;
FnCall              ::= identifier, "(", [ FnArguments ], ");
FnArguments         ::= Expression, { ",", Expression };
NewStruct           ::= VariantAccess, "{", { Assignment, ";" }, "}"
ReturnStatement     ::= "return", [ Expression ];
IfStatement         ::= "if", "(", Expression", ")", Block, [ "else", Block ];
WhileStatement      ::= "while", "(", Expression, ")", Block;
MatchStatement      ::= "match", "(", Expression, ")", "{", Matchers, "}";

Matchers            ::= Matcher, { Matcher };
Matcher             ::= Type, identifier, "=>", Block, ";";

Access              ::= identifier, { ".", identifier };
VariantAccess       ::= identifier, { "::", identifier };
Type                ::= builtin_type
                      | VariantAccess;

Expression          ::= AndExpression, { or_op, AndExpression };
AndExpression       ::= RelationExpression, { and_op, RelationExpression };
RelationExpression  ::= AdditiveTerm, [ relation_op, AdditiveTerm ];
AdditiveTerm        ::= MultiplicativeTerm, { additive_op, MultiplicativeTerm };
MultiplicativeTerm  ::= UnaryTerm, { multiplicative_op, UnaryTerm }
UnaryTerm           ::= [ unary_op ], CastedTerm;
CastedTerm          ::= Term, [ "is", Type ], [ "as", Type ];
Term                ::= literal
                       | Access
                       | FnCall
                       | NewStruct
                       | "(", Expression, ")";
```

## Obsługa błędów

### Lekser

- W przypadku napotkania nieprawidłowego symbolu lub ciągu znaków, lekser
  zgłasza błąd leksykalny `LexerError.UnexpectedCharacter`
- Lekser zgłasza błędy zbyt długiego identyfikatora: `IdentifierTooLongError`
- Lekser zgłasza błędy niezamkniętego ciągu
  znaków: `StringTooLongError`, `UnterminatedStringError`, `InvalidEscapeSequenceError`
- Zgłaszane błędy zawierają informację o położenie problematycznego znaku
- Zgłoszenie błędu kończy dalszą analizę programu

### Parser

- Parser zgłasza błędy związane z nieprawidłową składnią `ParserError`
- Błędy zawierają informacje o nieoczekiwanym tokenie, oczekiwanym tokenie oraz
  obowiązkowo o lokalizacji
- Zgłoszenie błędu kończy dalszą analizę programu

### Interpreter i analizatory semantyczne

- Interpreter uruchamia analizatory semantyczne przed wykonaniem kodu.
- Interpreter w przypadku wystąpienia błędu będzie wyrzucać stosowny wyjątek w
  zależności od błędu:
    - `MaximumRecursionError` w przypadku przekroczenia limitu rekursji
    - `PanicError` w przypadku wywołania mechanizmu panikowania.
    - `InternalError` w przypadku sytuacji błędnych, które wynikają z
      manipulowania wewnętrznym stanem interpretera.
- Błedy zawierają informację o położeniu oraz kontekst wystąpienia danego
  problemu np. `undefined name 'x'`.
- Zgłoszenie błędu kończy dalszą analizę program.
- Analizatory semantyczne wyrzucają stosowne wyjątki

### Mechanizm panikowania

- Mechanizm panikowania kończy interpretację programu oraz wyświetla stosowny
  komunikat np.: `panic!: unknown variable 'z' at <line>:<column>`.
- Mechanizm wykorzystywany jest przez funkcje wbudowane oraz może być używany
  przez użytkownika.

## Analiza wymagań funkcjonalnych

1. Interpreter musi przechowywać informacje o typie, mutowalności oraz wartości
   zmiennych.
    - Informacje o typie są wykorzystywane do dokonywania automatycznej
      konwersji typów, sprawdzania typów, rzutowania


2. Interpreter musi posiadać wbudowane funkcje konwersji typów pomiędzy typami
   wbudowanymi.

| from \ to | i32 | f32 | bool | str |
|-----------|-----|-----|------|-----|
| i32       |     | +   | *2   | +   |
| f32       | *1  |     | *2   | +   |  
| bool      | -   | -   |      | +   |  
| str       | -   | -   | *3   |     | 

*1 - konwersja może prowadzić do utraty danych

*2 - wartość prawda dla niezerowych wartości

*3 - wartość prawda dla niepustego ciągu znaków

3. Interpreter musi implementować podstawowe operacje dla typów wbudowanych.
    - Interpreter wyszukuje implementację danej operacji dla danych typów
      wejściowych.
    - W przypadku nie znalezienia takiej implementacji:
        - dla operacji boolowskich próbuje dokonać konwersji obu argumentów to
          typu `bool` a następnie wyszukuje implementacje dla tych argumentów
        - dla operacji porównania oraz binarnych próbuje dokonać
          konwersji drugiego argumentu tak, aby miał typ zgodny z pierwszym
          argumentem.
        - dla operacji unarnych wyrzuca wyjątek
        - dla operacji castowania wyrzuca wyjątek, jeżeli typ nie jest typem /
          dzieckiem typu do którego jest rzutowany

| operator(y) | argument  | argument  | typ zwracany |                                          
|-------------|-----------|-----------|--------------|
| && \|\|     | i32       | i32       | i32          |
| && \|\|     | f32       | f32       | f32          |
| && \|\|     | str       | str       | str          |
| && \|\|     | bool      | bool      | bool         |
| .           | .         | .         | .            |
| == !=       | i32       | i32       | bool         |
| == !=       | f32       | f32       | bool         |
| == !=       | str       | str       | bool         |
| == !=       | bool      | bool      | bool         |
| < >         | i32 / f32 | i32 / f32 | bool         |
| .           | .         | .         | .            |
| + - * /     | i32       | i32       | i32          |                                          
| + - * /     | f32       | f32       | f32          |
| +           | str       | str       | str          |             
| *           | str       | i32       | str          |       
| .           | .         | .         | .            |
| -           | i32       | .         | i32          |
| !           | bool      | .         | bool         |

4. Interpreter musi implementować podstawowe funkcje wbudowane.

| funkcja | argument(y) | typ zwracany | 
|---------|-------------|--------------|
| println | str         | -            |
| readI32 | -           | i32          |
| readStr | -           | str          |

# Rozwiązanie

## Skrócony opis implementacji

### Common

1. `Box`
    - Pudełko na przechowywane wartości.
    - Pozwala ustawiać, podglądać, zabierać, czyścić wartość.
    - Pozwala skonfigurować czyszczenie innych pudełek przy zabieraniu
      wartości.
2. `Location`
    - Reprezentuje lokację jako pewny obszar między dwoma pozycjami.
3. `Position`
    - Reprezentuje pozycję.
4. `Registrable`
    - Umożliwia wykonanie akcji na udekorowanych funkcjach.
5. `shall()`
    - Pozwala pobrać wartość, a w przypadku jej braku wyrzucić wyjątek.

### Lexer

1. `errors.py`
    - Zbiór wszystkich typów błędów, które mogą być rzucane przez lekser.
2. `iter.py`
    - Implementacja iteratora na lekserze - pozwala na pobieranie kolejnych
      tokenów.
3. `Lexer`
    - Analizator leksykalny pracujący na dowolnym buforze.
4. `Token`
    - Reprezentacja tokenu.
5. `TokenKind`
    - Reprezentacja typu tokenu.

### Parser

1. `ast/*.py`
    - Zbiór klas reprezentujących różne konstrukcje językowe.
2. `IFromTokenKind`
    - Interfejs definiujący typy operacji.
3. `ITreeLikeExpression`
    - Interfejs grupujący wyrażenia, które są drzewiaste.
4. `ebnf()`
    - Pomocniczy dekorator, który pozwala w sposób czytelny zapisać produkcję,
      która jest parsowana przez daną metodę.
5. `Parser`
    - Analizator składniowy produkujący drzewo składniowe gotowe do
      interpretacji.

### Tools

1. `Formatter`
    - Prosty, lecz niekompletny formater kodu.
2. `Printer`
    - Prosty wizytator, który pozwala na wyrysowanie drzewa składniowego w
      formie czytelnej dla człowieka.

### Utils

1. `StreamBuffer`
    - Implementacja strumienia znaków, która pozwala na działanie na ciągach
      znaków, plikach w trybie tekstowym i binarnym.
2. `StringBuilder`
    - Nakładka ułatwiająca budowanie ciągów znaków.

## Uzasadnienie decyzji implementacyjnych

1. Rezygnacja z dodatkowych typów danych
   W ramach projektu wstępnego planowane było więcej typów danych, jednak
   zrezygnowano z nich, ze względu, że ich implementacja byłaby żmudna i
   nakładała by dodatkowej pracy nie przynosząc realnych korzyści dla
   projektu - w docelowym zastosowaniu wszystkie typy reprezentowane miały być
   za pomocą 32 bitów

2. Reprezentacja wewnętrzna typów danych i32 i f32
   Typy danych `i32` oraz `f32` reprezentowane są wewnętrznie jako typy języka
   Python odpowiednio `int` oraz `float`, z tego powodu zmienne, które są tych
   typów zachowują się odpowiednio jak liczba całkowita o nieskończonej
   wielkości (`int` w Pythonie posiada nieskończoną wielkość, ograniczoną
   jedynie przez pamięć urządzenia) oraz liczbie zmiennoprzecinkowej 32- lub
   64-bitowej (w zależności od systemu operacyjnego)

3. Przeciążanie funkcji
   W projekcie wstępnym zakładane było przeciążanie funkcji, jednak
   implementacja przeciążania funkcji dokładały by dodatkowej pracy jak również
   stwarzały by problem rozwiązywania oraz zapisywania konwecji w przypadku
   przyjmowania wartości będących rekordami wariantowymi

## Problemy i trudności

### Lekser

1. Czytelna implementacja
    - Wykonanie czytelnej implementacji wymagało wielu zmian i przemyślenia
      przed realizacją kodu
2. Brak ujednoliconego streama do znaków

### Parser

1. Braki i błędy w gramatyce
    - Wynikające z braku doświadczenia, które udało się odnaleźć dopiero przy
      pisaniu implementacji, gdy kod wydawał się bezsensowny

### Interpreter

1. Gromadzenie informacji o typach
    - Gromadzenie ich w sposób elegancki wymagało kilkunastu godzin pracy, tak
      by rozwiązanie było zarówno czytelne, jak i wygodne dla użytkownika i
      programisty
2. Czytelny rejestr operacji
    - Czytelna rejestracja i przechowywanie dostępnych operacji pochłoneła
      również kilka godzin pracy
3. Przemyślana koncepcja i czytelna implementacja
    - Brak doświadczenia w pisaniu interpretera powodował, że trzeba było
      ciągle zmieniać swój kod, tak by był nadal czytelny pomimo dodawania
      dodatkowych funkcji

## Użycie

1. Uruchomienie interpretacji

```shell
python main.py execute --in main.fhll
```

---
