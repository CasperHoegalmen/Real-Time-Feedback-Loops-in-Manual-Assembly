using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class InstructionsScript : MonoBehaviour
{
    public int timerNum;

    public TextMeshProUGUI instructions;
    public bool timerFin;
    public bool startTheTimer;
    // Start is called before the first frame update
    void Start()
    {
        instructions = GetComponent<TextMeshProUGUI>();
        instructions.SetText("");
        //startTheTimer = true;
    }

    // Update is called once per frame
    void Update()
    {
        if(startTheTimer == true)
        {
            StartCoroutine(actuallyStartTimer());
            startTheTimer = false;
           

        }
    }

   
      

    IEnumerator actuallyStartTimer(){
        timerFin = false;
        timerNum = 3;
        instructions.SetText("Please remove your hand. Next step in " + timerNum +"...");
        yield return new WaitForSeconds(1);
        timerNum--;
        instructions.SetText("Please remove your hand. Next step in " + timerNum +"...");
        yield return new WaitForSeconds(1);
        timerNum--;
        instructions.SetText("Please remove your hand. Next step in " + timerNum +"...");
        yield return new WaitForSeconds(1);
        instructions.SetText("");
        timerFin = true;
        yield return new WaitForSeconds(1);
        timerFin = false;

    }

}
