using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using TMPro;

public class HelloClient : MonoBehaviour
{
    private HelloRequester _helloRequester;
    public bool SendPack = true;
    //[SerializeField] BrickChanger brick;
    [SerializeField] ImageChanger changeSprite;
    [SerializeField] BrickChanger brickChanger;
    bool correctColor = false, correctShape = false, correctPosition = false, correctHeight = false;
    bool trigger = true;
    bool run = true;
    int brick = 0;

    [SerializeField] private TextMeshProUGUI instructionsText;

    private void Start()
    {
        instructionsText = GameObject.Find("InstructionText").GetComponent<TextMeshProUGUI>();
        _helloRequester = new HelloRequester();
        //brick.GetComponent<BrickChanger>();
        _helloRequester.Start();
        _helloRequester.stepNumber = 0;
    }

    void Update()
    {
        if (SendPack)
        {
            _helloRequester.Continue();
        } else if (!SendPack)
        {
            _helloRequester.Pause();
        }

        ConditionsCheck();
    }

    public void ConditionsCheck()
    {
        //correctColor = false;
        //correctShape = false;

        if (run)
        {
            if (HelloRequester.errorFeedback[0] == "Correct")
            {
                changeSprite.ChangeImage(3, 1);
                correctColor = true;
            }
            else
            {
                changeSprite.ChangeImage(3, 0);
                correctColor = false;
            }

            if (HelloRequester.errorFeedback[1] == "Correct")
            {
                changeSprite.ChangeImage(1, 1);
                correctShape = true;
            }
            else
            {
                changeSprite.ChangeImage(1, 0);
                correctShape = false;
            }

            if (HelloRequester.errorFeedback[2] == "Correct")
            {
                changeSprite.ChangeImage(0, 1);
                correctPosition = true;
            }
            else
            {
                changeSprite.ChangeImage(0, 0);
                correctPosition = false;
            }

            if(HelloRequester.errorFeedback[3] == "Correct")
            {
                changeSprite.ChangeImage(2, 1);
                correctHeight = true;
            }
            else
            {
                changeSprite.ChangeImage(2, 0);
                correctHeight = false;
            }
        }

        Debug.Log(correctColor + " " + correctShape + " " + correctPosition);
        if (trigger)
        {
            if (correctColor && correctShape && correctPosition && correctHeight)
            {
                trigger = false;
                //correctColor = false;
                //correctShape = false;
           
                StartCoroutine(changeToNextBrick(brick));
                brick++;
            }
        }
    }

    private IEnumerator changeToNextBrick(int brick)
    {
        _helloRequester.stepNumber++;
        run = false;
        int timerNum = 3;
        instructionsText.SetText("Please remove your hand. Next step in " + timerNum + "...");
        yield return new WaitForSeconds(1);
        timerNum--;
        instructionsText.SetText("Please remove your hand. Next step in " + timerNum + "...");
        yield return new WaitForSeconds(1);
        timerNum--;
        instructionsText.SetText("Please remove your hand. Next step in " + timerNum + "...");
        yield return new WaitForSeconds(1);
        instructionsText.SetText("");      
        run = true;
        //Debug.Log(_helloRequester.stepNumber);
        brickChanger.ChangeMaterial(brick, "opaque");
        brickChanger.EnableBrick(brick + 1);
        trigger = true;
    }

    private void OnDestroy()
    {
        _helloRequester.Stop();
    }
}
