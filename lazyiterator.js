/*
    = LAZY ITERATOR =
    When using filter and map on javascript lists you copy the entire list for every single time you apply a map or filter. 
    I thought that was annoyingly inefficent, so I wrote a lazy iterator that lets you apply both map and filter.
    It does this without mutating the original list, and it doesnt apply the mapping function or predicate for filtering before 
    you try to access the element.
*/


/* Allows javascript lists to get a method that returns it as a lazyIterator */
Array.prototype.lazyIterator = function(){
    return new Lazyiterator(this)
}

class Lazyiterator {
    constructor(iterable) {
        this.iterable = iterable;
        this.operations = [];
        this.index = 0;
    }

    [Symbol.iterator]() {
        return this;
    }

    next() {

        while (this.index < this.iterable.length) {
            const currentValue = this.iterable[this.index++];
            const mappedValue = this.operations.reduce(
                (value, operation) => operation(value),
                currentValue
            );
            /* 
                We might both get undefined and NaN. The best way of checking for 
                NaN is checking for self equality.
             */
            if (mappedValue !== undefined && mappedValue === mappedValue) {
                return { value: mappedValue, done: false };
            }
        }

        return { done: true };
    }

    map(unaryFunc) {
        this.operations.push((x) => unaryFunc(x));
        return this;
    }

    filter(predicate) {
        this.operations.push((x) => (predicate(x) 
            ? x 
            : undefined));
        return this;
    }

    forEach(unaryFunc){
        let element = this.next();
        while(!element.done){
            unaryFunc(element.value);
            element = this.next();
        }
    }

    take(n) {
        const takenElements = [];
        while(this.index < this.iterable.length && 0 < n--){
            const valueDoneObject = this.next();
            if (valueDoneObject.done) return takenElements;
            takenElements.push(valueDoneObject.value);
        }
        return takenElements;
    }
}
