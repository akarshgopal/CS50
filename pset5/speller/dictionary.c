/**
 * Implements a dictionary's functionality.
 */
#include "dictionary.h"

//Structure for Trie
typedef struct wordpart{
    bool exists;
    struct wordpart *next[27];

}wrd;

wrd *dict,*curr;

int dictsize = 0;
bool loaded = 0;

//Free function iterates over each letter and unloads from end
void freeword(wrd* dict2)
{
    if(loaded)      //check if dictionary is loaded
    {
        wrd *curr =dict2;
        for(int i = 0; i < 27; i++)
        {

            if (curr -> next[i] != NULL)
            {
                freeword(curr -> next[i]);
            }

        }
        free(dict2);
        return;
    }
}



/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // TODO
    int inta = (int)'a';
    int intz = (int)'z';

    // set current node to root node
    wrd* curr = dict;

    // looping through each letter in word
    int i = 0;
    //printf("checking %s\t",word);
    while(word[i] != '\0')
    {
        char ch = word[i];


        // find is ch is apostrophe
        if (word[i] == '\'')
        {
            ch = intz + 1;
        }
        // converting letter between 0 and 25
        int nextindex = tolower(ch) - inta;

        if (curr -> next[nextindex] != NULL)
        {
            curr = curr -> next[nextindex];
            i++;
           // printf("%c",ch);
        }
        else
        {
            return false;
        }

    }
        //printf("\n");
        if (curr -> exists == true)
        {
            return true;
        }
        else
        {
            return false;
        }

}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // integer mapping for a and z
   int inta = (int)'a';
   int intz = (int)'z';

   // opening the dictionary file
   FILE* fp = fopen(dictionary,"r");

   // sanity check for null returned reference
   if (fp == NULL)
   {
    return false;
   }

   // mallocing memory for first node
   dict = (wrd*)malloc(sizeof(wrd));
   for(int i=0;i<27;i++){
       dict->next[i]=NULL;
   }

   // integer for current position in children array
   int character = 0;

   // cursor node

   // looping through dictionary until end of file is encountered
   while(EOF != (character = fgetc(fp)))
   {
   		// setting current node to first node
   		curr = dict;
        //printf("added\t");

   		// iterating through character and adding each letter to next until "\n"
   		do
   		{
   			// if apostrophe then store in
   			if (character == '\'')
   			{
   				character = intz + 1;
   			}

   			// if the character is not in trie...create one
   			if (curr -> next[character -inta] == NULL)
   			{
   				// malloc a new node

   				curr -> next[character - inta] = (wrd*)malloc(sizeof(wrd));
   				curr = curr -> next[character - inta];
   			    for(int i=0;i<27;i++)
   			    {
                        curr->next[i]=NULL;
                }
                curr->exists=false;
   			}
   			// got to address in children
   			else
   			{
   				curr = curr -> next[character - inta];
   			}

   		}while(((character = fgetc(fp)) != '\n'));
   		//printf("\n");
        curr -> exists = true;

   		dictsize++;
   }
   // close the dictionary file
   fclose(fp);
   loaded = true;
   return loaded;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // TODO
    return dictsize;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    wrd* curr= dict;
    freeword(curr);
    return true;
}


