using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using AsyncIO;
using NetMQ;
using NetMQ.Sockets;

public class HelloClient : MonoBehaviour
{
    private HelloRequester _helloRequester;
    public bool SendPack = true;
    //[SerializeField] BrickChanger brick;
    [SerializeField] ImageChanger changeSprite;
    [SerializeField] BrickChanger brickChanger;
    bool correctColor = false, correctShape = false, correctPosition = false;
    bool trigger = true;
    bool run = true;
    int brick = 0;
    
    private void Start()
    {
        _helloRequester = new HelloRequester();
        //brick.GetComponent<BrickChanger>();
        _helloRequester.Start();
        _helloRequester.stepNumber = 1;
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
        }

        Debug.Log(correctColor + " " + correctShape + " " + correctPosition);
        if (trigger)
        {
            if (correctColor && correctShape && correctPosition)
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
        yield return new WaitForSeconds(2);
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