using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class InstructionsScript : MonoBehaviour
{
    public int timerNum;

    public TextMeshProUGUI instructions;
    public bool timerFin;
    // Start is called before the first frame update
    void Start()
    {
        instructions = GetComponent<TextMeshProUGUI>();
        this.gameObject.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
    }

    public void startTimer(){
        StartCoroutine(actuallyStartTimer());
    }

    IEnumerator actuallyStartTimer(){
        this.gameObject.SetActive(true);
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
        this.gameObject.SetActive(false);
        timerFin = true;
        yield return new WaitForSeconds(1);
        timerFin = false;

    }

}
